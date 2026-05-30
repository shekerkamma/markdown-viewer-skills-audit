import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from app.services.event_logger import EventLogger


@dataclass
class AgentResult:
    success: bool
    output: dict | str | None = None
    confidence: float = 0.0
    error: str | None = None
    tokens_used: int = 0


class BaseAgent(ABC):
    name: str = "base"

    def __init__(self, pipeline_run_id: uuid.UUID, event_logger: EventLogger):
        self.pipeline_run_id = pipeline_run_id
        self.event_logger = event_logger

    async def log_action(self, action_type: str, payload: dict) -> None:
        await self.event_logger.log(
            pipeline_run_id=self.pipeline_run_id,
            agent_name=self.name,
            event_type="action",
            payload={"action_type": action_type, **payload},
        )

    async def log_observation(self, observation: str) -> None:
        await self.event_logger.log(
            pipeline_run_id=self.pipeline_run_id,
            agent_name=self.name,
            event_type="observation",
            payload={"observation": observation},
        )

    async def log_decision(self, decision: str, confidence: float) -> None:
        await self.event_logger.log(
            pipeline_run_id=self.pipeline_run_id,
            agent_name=self.name,
            event_type="decision",
            payload={"decision": decision, "confidence": confidence},
        )

    async def log_error(self, error: str) -> None:
        await self.event_logger.log(
            pipeline_run_id=self.pipeline_run_id,
            agent_name=self.name,
            event_type="error",
            payload={"error": error},
        )

    @abstractmethod
    async def run(self, context: dict) -> AgentResult:
        pass
