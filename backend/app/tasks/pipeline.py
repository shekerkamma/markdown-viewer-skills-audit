import logging

logger = logging.getLogger(__name__)


async def run_pipeline(ctx: dict, ticket_id: str) -> str:
    logger.info("Pipeline started for ticket %s", ticket_id)
    return f"Pipeline completed for ticket {ticket_id}"
