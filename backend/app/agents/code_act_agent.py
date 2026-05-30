import asyncio
import logging
import uuid

from app.agents.base import AgentResult, BaseAgent
from app.services.claude_service import ClaudeService
from app.services.docker_service import DockerService
from app.services.event_logger import EventLogger

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert software engineer fixing a bug in a codebase. You have been given:
1. A structured analysis of the bug from a ticket analyst
2. The contents of the relevant source files

Your task: generate a minimal, correct fix for the described bug. Follow these rules:
- Make the smallest possible change that fixes the issue
- Maintain the existing code style
- Add or update tests to cover the fix
- If you need to see more files, say which files you need
- Output your fix as a unified diff (the kind you'd get from `git diff`)

Output format:
1. Brief explanation of the fix (2-3 sentences max)
2. The complete unified diff

Do NOT wrap the diff in markdown code fences."""

MAX_ITERATIONS = 3
TIMEOUT_SECONDS = 300


class CodeActAgent(BaseAgent):
    name = "code_act_agent"

    def __init__(
        self,
        pipeline_run_id: uuid.UUID,
        event_logger: EventLogger,
        claude_service: ClaudeService,
        docker_service: DockerService,
    ):
        super().__init__(pipeline_run_id, event_logger)
        self.claude = claude_service
        self.docker = docker_service

    async def run(self, context: dict) -> AgentResult:
        analysis = context.get("analysis", {})
        repo_url = context.get("repo_url", "")
        branch = context.get("branch", "main")
        github_token = context.get("github_token", "")

        await self.log_action("start_code_generation", {
            "repo_url": repo_url,
            "branch": branch,
            "affected_files": analysis.get("affected_files", []),
        })

        container_id = None
        try:
            # Create sandbox
            container_id = await self.docker.create_sandbox(repo_url, branch)
            await self.log_action("sandbox_created", {"container_id": container_id[:12]})

            # Read affected files
            affected_files = analysis.get("affected_files", [])
            file_contents = {}
            for file_path in affected_files:
                content = await self.docker.exec_in_sandbox(
                    container_id,
                    f"cat /workspace/repo/{file_path} 2>/dev/null || echo 'FILE NOT FOUND'",
                )
                file_contents[file_path] = content

            await self.log_observation(
                f"Read {len(file_contents)} files from sandbox"
            )

            # If no files specified, try to find relevant files from the problem
            if not file_contents:
                ls_output = await self.docker.exec_in_sandbox(
                    container_id,
                    "cd /workspace/repo && find . -name '*.py' -o -name '*.ts' -o -name '*.js' "
                    "| head -50",
                )
                await self.log_observation(f"Listed project files for context: {len(ls_output.splitlines())} files")

            # Generate fix with iteration
            fix_diff = None
            for iteration in range(1, MAX_ITERATIONS + 1):
                await self.log_action("generate_fix", {"iteration": iteration})

                files_context = "\n\n".join(
                    f"--- {path} ---\n{content}" for path, content in file_contents.items()
                )

                user_prompt = f"""Bug Analysis:
Problem: {analysis.get('problem_statement', 'Unknown')}
Severity: {analysis.get('severity', 'unknown')}
Affected files: {', '.join(analysis.get('affected_files', ['unknown']))}
Reproduction steps: {chr(10).join(analysis.get('reproduction_steps', ['Not provided']))}

Source Files:
{files_context or 'No specific files identified. Use the problem description to determine which files to fix.'}

{"Previous iteration failed tests. Please fix the remaining issues." if iteration > 1 else ""}"""

                response = await self.claude.generate_code(
                    system_prompt=SYSTEM_PROMPT,
                    user_prompt=user_prompt,
                )

                # Apply the generated fix in the sandbox
                await self.docker.exec_in_sandbox(
                    container_id,
                    f"cd /workspace/repo && cat << 'PATCH_EOF' | git apply --allow-empty -\n{response}\nPATCH_EOF",
                )

                # Run tests
                test_output = await self.docker.exec_in_sandbox(
                    container_id,
                    "cd /workspace/repo && python -m pytest --tb=short -q 2>&1 || "
                    "npm test 2>&1 || echo 'NO_TEST_RUNNER'",
                )

                await self.log_observation(f"Test run (iteration {iteration}): {test_output[:500]}")

                if "FAILED" not in test_output and "ERROR" not in test_output:
                    fix_diff = await self.docker.get_diff(container_id)
                    await self.log_decision(
                        f"Fix generated and tests pass (iteration {iteration})",
                        0.8,
                    )
                    break

                await self.log_observation(f"Tests failed on iteration {iteration}, retrying...")

            if not fix_diff:
                fix_diff = await self.docker.get_diff(container_id)

            if not fix_diff or fix_diff.strip() == "":
                await self.log_error("No changes generated after all iterations")
                return AgentResult(
                    success=False,
                    error="Failed to generate a valid fix after all iterations",
                    tokens_used=self.claude.total_tokens_used,
                )

            return AgentResult(
                success=True,
                output={"diff": fix_diff, "iterations": iteration},
                confidence=0.7 if iteration == 1 else 0.5,
                tokens_used=self.claude.total_tokens_used,
            )

        except asyncio.TimeoutError:
            await self.log_error(f"Sandbox timed out after {TIMEOUT_SECONDS}s")
            return AgentResult(
                success=False,
                error=f"Sandbox execution timed out after {TIMEOUT_SECONDS} seconds",
                tokens_used=self.claude.total_tokens_used,
            )
        except Exception as e:
            await self.log_error(f"CodeActAgent failed: {e}")
            return AgentResult(
                success=False,
                error=str(e),
                tokens_used=self.claude.total_tokens_used,
            )
        finally:
            if container_id:
                await self.docker.destroy_sandbox(container_id)
                await self.log_action("sandbox_destroyed", {"container_id": container_id[:12]})
