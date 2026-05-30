import logging

import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings

logger = logging.getLogger(__name__)


class ClaudeService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self._total_input_tokens = 0
        self._total_output_tokens = 0

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=30))
    async def analyze(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "claude-sonnet-4-20250514",
    ) -> str:
        response = self.client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        self._track_usage(response.usage)
        return response.content[0].text

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=30))
    async def generate_code(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "claude-opus-4-20250514",
    ) -> str:
        response = self.client.messages.create(
            model=model,
            max_tokens=8192,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        self._track_usage(response.usage)
        return response.content[0].text

    def _track_usage(self, usage) -> None:
        self._total_input_tokens += usage.input_tokens
        self._total_output_tokens += usage.output_tokens
        logger.debug(
            "Token usage: input=%d, output=%d (total: %d/%d)",
            usage.input_tokens,
            usage.output_tokens,
            self._total_input_tokens,
            self._total_output_tokens,
        )

    @property
    def total_tokens_used(self) -> int:
        return self._total_input_tokens + self._total_output_tokens
