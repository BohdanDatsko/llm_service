"""Implementation of an LLM client that calls the OpenAI API"""

from __future__ import annotations

import asyncio

from openai import OpenAI

from llm_service.clients import LLMClient
from llm_service.config import get_settings


class OpenAIClient(LLMClient):
    """LLM client that delegates requests to OpenAI using the new (>=1.x) SDK.

    Notes:
        * The OpenAI 1.x SDK exposes synchronous methods. Since our interface is
          async, we run those calls in a thread via `asyncio.to_thread`.
        * `base_url` is optional and should only be set for custom gateways
          (e.g., proxy, Azure-compatible endpoint). For regular OpenAI usage,
          leave it unset so the SDK uses https://api.openai.com/v1.
    """

    def __init__(self, model: str = "gpt-4o") -> None:
        settings = get_settings()

        if not settings.OPENAI_API_KEY:
            raise ValueError(
                "OpenAI API key is missing. Set OPENAI_API_KEY in your environment or .env file."
            )

        # Initialize a dedicated client instance (no global state).
        # base_url remains None for the default OpenAI endpoint.
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL or None,
        )
        self.model = model

    async def generate(self, prompt: str) -> str:
        """Generate a completion using the OpenAI Responses API.

        The SDK 1.x is synchronous, so delegate to a worker thread to avoid
        blocking the event loop.
        """

        def _call() -> str:
            # Responses API (recommended in SDK 1.x).
            resp = self.client.responses.create(
                model=self.model,
                input=prompt,
                # You may tweak instructions or provide system context here:
                instructions="You are a helpful coding assistant.",
            )
            # `output_text` provides a convenient flattened text representation.
            return resp.output_text

        return await asyncio.to_thread(_call)
