import json
import logging
import uuid

from app.agents.base import AgentResult, BaseAgent
from app.services.claude_service import ClaudeService
from app.services.event_logger import EventLogger

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a bug ticket analyst for an automated code fix pipeline. Your job is to analyze a GitHub Issue and extract structured information that downstream agents will use to generate a fix.

Analyze the issue and output ONLY valid JSON with this exact structure:
{
  "problem_statement": "A clear, concise description of what is broken",
  "affected_files": ["list of file paths mentioned or implied"],
  "reproduction_steps": ["step 1", "step 2", ...],
  "severity": "low" | "medium" | "high" | "critical",
  "confidence": 0.0-1.0
}

Guidelines:
- If the issue body is empty or very minimal, set confidence below 0.4
- If no files are mentioned, leave affected_files as an empty array
- If no reproduction steps are provided, infer them if possible or leave empty
- Severity: critical = data loss/security, high = feature broken, medium = degraded functionality, low = cosmetic/minor
- Confidence reflects how well you understand the problem AND how likely it is that an automated fix can be generated
- Output ONLY the JSON, no markdown code fences, no explanation"""


class ContentResearcherAgent(BaseAgent):
    name = "content_researcher"

    def __init__(
        self,
        pipeline_run_id: uuid.UUID,
        event_logger: EventLogger,
        claude_service: ClaudeService,
    ):
        super().__init__(pipeline_run_id, event_logger)
        self.claude = claude_service

    async def run(self, context: dict) -> AgentResult:
        title = context.get("title", "")
        body = context.get("body", "")
        labels = context.get("labels", [])

        await self.log_action("analyze_ticket", {
            "title": title,
            "body_length": len(body) if body else 0,
            "labels": labels,
        })

        user_prompt = f"""GitHub Issue #{context.get('issue_number', '?')}

Title: {title}

Labels: {', '.join(labels) if labels else 'none'}

Body:
{body or '(no body provided)'}"""

        try:
            response = await self.claude.analyze(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
            )

            # Parse the JSON response
            analysis = json.loads(response.strip())

            await self.log_observation(
                f"Analysis complete: severity={analysis.get('severity')}, "
                f"confidence={analysis.get('confidence')}, "
                f"affected_files={len(analysis.get('affected_files', []))}"
            )

            confidence = analysis.get("confidence", 0.0)

            if confidence < 0.4:
                await self.log_decision(
                    f"Low confidence ({confidence}). Recommending escalation.",
                    confidence,
                )
                return AgentResult(
                    success=False,
                    output=analysis,
                    confidence=confidence,
                    error=f"Low confidence analysis ({confidence}). "
                    f"Reason: insufficient information to generate a fix.",
                    tokens_used=self.claude.total_tokens_used,
                )

            await self.log_decision(
                f"Analysis confident ({confidence}). Proceeding to code generation.",
                confidence,
            )

            return AgentResult(
                success=True,
                output=analysis,
                confidence=confidence,
                tokens_used=self.claude.total_tokens_used,
            )

        except json.JSONDecodeError as e:
            await self.log_error(f"Failed to parse Claude response as JSON: {e}")
            return AgentResult(
                success=False,
                error=f"Failed to parse analysis response: {e}",
                tokens_used=self.claude.total_tokens_used,
            )
        except Exception as e:
            await self.log_error(f"Content researcher failed: {e}")
            return AgentResult(
                success=False,
                error=str(e),
                tokens_used=self.claude.total_tokens_used,
            )
