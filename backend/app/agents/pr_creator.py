import logging
import time
import uuid

from app.agents.base import AgentResult, BaseAgent
from app.services.docker_service import DockerService
from app.services.event_logger import EventLogger
from app.services.github_service import GitHubService

logger = logging.getLogger(__name__)


class PRCreatorAgent(BaseAgent):
    name = "pr_creator"

    def __init__(
        self,
        pipeline_run_id: uuid.UUID,
        event_logger: EventLogger,
        docker_service: DockerService,
        github_service: GitHubService,
    ):
        super().__init__(pipeline_run_id, event_logger)
        self.docker = docker_service
        self.github = github_service

    async def run(self, context: dict) -> AgentResult:
        repo_full_name = context.get("repo_full_name", "")
        repo_url = context.get("repo_url", "")
        issue_number = context.get("issue_number", 0)
        diff = context.get("diff", "")
        analysis = context.get("analysis", {})
        review = context.get("review", {})
        github_token = context.get("github_token", "")

        branch_name = f"ticketforge/fix-{issue_number}"
        # Handle branch name conflicts by appending timestamp
        branch_name_with_ts = branch_name

        await self.log_action("create_pr", {
            "repo": repo_full_name,
            "issue_number": issue_number,
            "branch": branch_name,
        })

        container_id = None
        try:
            # Create sandbox, clone repo, apply fix, push
            container_id = await self.docker.create_sandbox(repo_url, "main")
            await self.log_action("sandbox_created", {"container_id": container_id[:12]})

            # Apply the diff
            apply_result = await self.docker.exec_in_sandbox(
                container_id,
                f"cd /workspace/repo && cat << 'PATCH_EOF' | git apply --allow-empty -\n{diff}\nPATCH_EOF",
            )

            # Create branch
            checkout_result = await self.docker.exec_in_sandbox(
                container_id,
                f"cd /workspace/repo && git checkout -b {branch_name}",
            )
            if "already exists" in checkout_result:
                branch_name_with_ts = f"{branch_name}-{int(time.time())}"
                await self.docker.exec_in_sandbox(
                    container_id,
                    f"cd /workspace/repo && git checkout -b {branch_name_with_ts}",
                )
                await self.log_observation(f"Branch conflict, using {branch_name_with_ts}")

            # Commit
            problem = analysis.get("problem_statement", f"Fix issue #{issue_number}")
            commit_msg = f"fix: {problem}"
            await self.docker.exec_in_sandbox(
                container_id,
                f'cd /workspace/repo && git add -A && git commit -m "{commit_msg}"',
            )

            # Configure git credentials and push
            await self.docker.exec_in_sandbox(
                container_id,
                f"cd /workspace/repo && git remote set-url origin "
                f"https://x-access-token:{github_token}@github.com/{repo_full_name}.git",
            )

            # Fetch latest main and attempt rebase if target branch updated
            await self.docker.exec_in_sandbox(
                container_id,
                f"cd /workspace/repo && git remote set-url origin "
                f"https://x-access-token:{github_token}@github.com/{repo_full_name}.git",
            )
            fetch_result = await self.docker.exec_in_sandbox(
                container_id,
                "cd /workspace/repo && git fetch origin main 2>&1",
            )
            rebase_result = await self.docker.exec_in_sandbox(
                container_id,
                "cd /workspace/repo && git rebase origin/main 2>&1",
            )
            if "CONFLICT" in rebase_result:
                await self.docker.exec_in_sandbox(
                    container_id,
                    "cd /workspace/repo && git rebase --abort",
                )
                await self.log_error("Rebase conflicts with updated target branch")
                return AgentResult(
                    success=False,
                    error="Target branch updated since clone and rebase has conflicts. Escalating.",
                )

            push_result = await self.docker.exec_in_sandbox(
                container_id,
                f"cd /workspace/repo && git push origin {branch_name_with_ts}",
            )

            if "Permission" in push_result or "denied" in push_result:
                await self.log_error(f"Push denied: {push_result}")
                return AgentResult(
                    success=False,
                    error=f"Push permission denied for {repo_full_name}",
                )

            await self.log_observation(f"Branch {branch_name_with_ts} pushed successfully")

            # Create PR
            pr_body = self._build_pr_body(issue_number, analysis, review)
            pr_title = f"fix: {problem}"
            if len(pr_title) > 70:
                pr_title = pr_title[:67] + "..."

            try:
                pr_data = await self.github.create_pr(
                    repo=repo_full_name,
                    branch=branch_name_with_ts,
                    title=pr_title,
                    body=pr_body,
                    token=github_token,
                )
            except Exception as e:
                # Retry once on API error
                await self.log_observation(f"PR creation failed, retrying: {e}")
                pr_data = await self.github.create_pr(
                    repo=repo_full_name,
                    branch=branch_name_with_ts,
                    title=pr_title,
                    body=pr_body,
                    token=github_token,
                )

            pr_number = pr_data.get("number")
            pr_url = pr_data.get("html_url")

            await self.log_decision(
                f"PR #{pr_number} created: {pr_url}",
                0.9,
            )

            return AgentResult(
                success=True,
                output={
                    "pr_number": pr_number,
                    "pr_url": pr_url,
                    "branch": branch_name_with_ts,
                },
                confidence=0.9,
            )

        except Exception as e:
            await self.log_error(f"PR creation failed: {e}")
            return AgentResult(
                success=False,
                error=str(e),
            )
        finally:
            if container_id:
                await self.docker.destroy_sandbox(container_id)
            await self.github.close()

    def _build_pr_body(
        self,
        issue_number: int,
        analysis: dict,
        review: dict,
    ) -> str:
        lines = [
            f"Fixes #{issue_number}",
            "",
            "## Summary",
            "",
            analysis.get("problem_statement", "Bug fix generated by TicketForge."),
            "",
        ]

        if analysis.get("affected_files"):
            lines.append("## Files Changed")
            lines.append("")
            for f in analysis["affected_files"]:
                lines.append(f"- `{f}`")
            lines.append("")

        if review.get("summary"):
            lines.append("## Review Assessment")
            lines.append("")
            lines.append(review["summary"])
            lines.append("")

        dimensions = review.get("dimensions", {})
        if dimensions:
            lines.append("| Dimension | Score |")
            lines.append("|-----------|-------|")
            for dim, data in dimensions.items():
                score = data.get("score", 0)
                lines.append(f"| {dim.title()} | {score:.1f} |")
            lines.append("")

        lines.append("---")
        lines.append("*Generated by [TicketForge](https://github.com/ticketforge) — AI-powered ticket-to-PR pipeline*")

        return "\n".join(lines)
