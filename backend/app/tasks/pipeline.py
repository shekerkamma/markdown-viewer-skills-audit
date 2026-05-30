import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy import select

from app.db import async_session_factory
from app.models.pipeline_run import PipelineRun
from app.models.repository import Repository
from app.models.ticket import Ticket
from app.models.user import User
from app.models.team import Team
from app.agents.content_researcher import ContentResearcherAgent
from app.agents.code_act_agent import CodeActAgent
from app.agents.escalation import EscalationHandler
from app.services.claude_service import ClaudeService
from app.services.docker_service import DockerService
from app.services.event_logger import EventLogger

logger = logging.getLogger(__name__)


async def run_pipeline(ctx: dict, ticket_id: str) -> str:
    logger.info("Pipeline started for ticket %s", ticket_id)

    async with async_session_factory() as session:
        # Load ticket
        result = await session.execute(
            select(Ticket).where(Ticket.id == uuid.UUID(ticket_id))
        )
        ticket = result.scalar_one_or_none()
        if not ticket:
            logger.error("Ticket %s not found", ticket_id)
            return f"Ticket {ticket_id} not found"

        # Load repository
        result = await session.execute(
            select(Repository).where(Repository.id == ticket.repository_id)
        )
        repo = result.scalar_one_or_none()

        # Load team owner for GitHub token
        result = await session.execute(
            select(User)
            .join(Team, Team.owner_id == User.id)
            .where(Team.id == repo.team_id)
        )
        owner = result.scalar_one_or_none()
        github_token = owner.github_access_token if owner else ""

        # Create pipeline run
        pipeline_run = PipelineRun(
            ticket_id=ticket.id,
            status="running",
        )
        session.add(pipeline_run)
        await session.commit()
        await session.refresh(pipeline_run)

        # Update ticket status
        ticket.status = "analyzing"
        await session.commit()

        event_logger = EventLogger(session)
        claude_service = ClaudeService()
        escalation = EscalationHandler(pipeline_run.id, event_logger)

        # --- Step 1: Content Analysis ---
        researcher = ContentResearcherAgent(pipeline_run.id, event_logger, claude_service)
        analysis_result = await researcher.run({
            "title": ticket.title,
            "body": ticket.body,
            "labels": ticket.labels,
            "issue_number": ticket.github_issue_number,
        })

        pipeline_run.analysis = analysis_result.output if isinstance(analysis_result.output, dict) else {}
        pipeline_run.tokens_used = analysis_result.tokens_used

        if not analysis_result.success:
            # Escalate
            ticket.status = "escalated"
            pipeline_run.status = "escalated"
            pipeline_run.escalation_reason = analysis_result.error
            pipeline_run.completed_at = datetime.now(timezone.utc)
            await session.commit()

            await escalation.escalate(
                repo_full_name=repo.full_name,
                issue_number=ticket.github_issue_number,
                github_token=github_token,
                agent_name="content_researcher",
                reason=analysis_result.error or "Low confidence analysis",
                partial_analysis=analysis_result.output,
            )
            return f"Ticket {ticket_id} escalated: {analysis_result.error}"

        # --- Step 2: Code Generation ---
        ticket.status = "generating"
        await session.commit()

        docker_service = DockerService()
        code_agent = CodeActAgent(pipeline_run.id, event_logger, claude_service, docker_service)
        fix_result = await code_agent.run({
            "analysis": analysis_result.output,
            "repo_url": f"https://github.com/{repo.full_name}.git",
            "branch": "main",
            "github_token": github_token,
        })

        pipeline_run.tokens_used = fix_result.tokens_used

        if not fix_result.success:
            ticket.status = "escalated"
            pipeline_run.status = "escalated"
            pipeline_run.escalation_reason = fix_result.error
            pipeline_run.completed_at = datetime.now(timezone.utc)
            await session.commit()

            await escalation.escalate(
                repo_full_name=repo.full_name,
                issue_number=ticket.github_issue_number,
                github_token=github_token,
                agent_name="code_act_agent",
                reason=fix_result.error or "Failed to generate fix",
                partial_analysis=analysis_result.output,
            )
            return f"Ticket {ticket_id} escalated: {fix_result.error}"

        # Save the diff
        fix_output = fix_result.output if isinstance(fix_result.output, dict) else {}
        pipeline_run.fix_diff = fix_output.get("diff", "")

        # Mark as done (review + PR creation handled in Phase 2)
        ticket.status = "generating"  # Will become "reviewing" in Phase 2
        pipeline_run.status = "completed"
        pipeline_run.completed_at = datetime.now(timezone.utc)
        if pipeline_run.started_at:
            delta = pipeline_run.completed_at - pipeline_run.started_at
            pipeline_run.duration_seconds = int(delta.total_seconds())
        await session.commit()

        logger.info("Pipeline completed for ticket %s — fix generated", ticket_id)
        return f"Pipeline completed for ticket {ticket_id}"
