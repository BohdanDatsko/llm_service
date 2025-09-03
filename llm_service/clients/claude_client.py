"""Implementation of an LLM client for Anthropic Claude (anthropic SDK)."""

from __future__ import annotations

import asyncio
import anthropic  # pip install anthropic

from llm_service.clients import LLMClient
from llm_service.config import get_settings


class ClaudeClient(LLMClient):
    """LLM client that calls Anthropic Claude via the anthropic SDK.

    Notes:
        * The anthropic SDK is synchronous; call inside a worker thread.
        * You must provide ANTHROPIC_API_KEY in the environment/.env.
        * Default model can be overridden via the constructor.
    """

    def __init__(self, model: str = "claude-3-5-sonnet-20240620", max_tokens: int = 1024):
        settings = get_settings()
        if not getattr(settings, "ANTHROPIC_API_KEY", None):
            raise ValueError(
                "Anthropic API key is missing. Set ANTHROPIC_API_KEY in your environment or .env file."
            )
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = model
        self.max_tokens = max_tokens

    @staticmethod
    def _extract_text(message) -> str:
        """Flatten the Claude message content into plain text."""
        parts = []
        for block in (message.content or []):
            if block.type == "text" and block.text:
                parts.append(block.text)
        return "\n".join(parts).strip()

    async def generate(self, prompt: str) -> str:
        """Generate a completion using Messages API."""
        def _call() -> str:
            msg = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return self._extract_text(msg)

        return await asyncio.to_thread(_call)
