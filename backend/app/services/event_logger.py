import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event

logger = logging.getLogger(__name__)


class EventLogger:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log(
        self,
        pipeline_run_id: uuid.UUID,
        agent_name: str,
        event_type: str,
        payload: dict,
    ) -> Event:
        event = Event(
            pipeline_run_id=pipeline_run_id,
            agent_name=agent_name,
            event_type=event_type,
            payload=payload,
            timestamp=datetime.now(timezone.utc),
        )
        self.session.add(event)
        await self.session.commit()
        logger.debug(
            "Event logged: run=%s agent=%s type=%s",
            pipeline_run_id,
            agent_name,
            event_type,
        )
        return event

    async def get_events(self, pipeline_run_id: uuid.UUID) -> list[Event]:
        result = await self.session.execute(
            select(Event)
            .where(Event.pipeline_run_id == pipeline_run_id)
            .order_by(Event.timestamp)
        )
        return list(result.scalars().all())
