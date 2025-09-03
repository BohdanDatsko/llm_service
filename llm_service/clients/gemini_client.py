"""Implementation of an LLM client for Google Gemini (google-generativeai SDK)."""

from __future__ import annotations

import asyncio

import google.generativeai as genai  # pip install google-generativeai

from llm_service.clients import LLMClient
from llm_service.config import get_settings


class GeminiClient(LLMClient):
    """LLM client that calls Google Gemini via google-generativeai SDK.

    Notes:
        * google-generativeai functions are synchronous; we call them in a thread.
        * For standard usage only an API key is needed (GEMINI_API_KEY).
        * Default model can be overridden via constructor.
    """

    def __init__(self, model: str = "gemini-2.0-flash-lite"):
        settings = get_settings()
        if not getattr(settings, "GEMINI_API_KEY", None):
            raise ValueError(
                "Gemini API key is missing. Set GEMINI_API_KEY in your environment or .env file."
            )
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = model

    async def generate(self, prompt: str) -> str:
        """Generate a completion using Gemini's GenerativeModel.generate_content()."""

        def _call() -> str:
            model = genai.GenerativeModel(self.model)
            resp = model.generate_content(prompt)
            # The SDK returns a rich object; `.text` provides the main text output.
            return (resp.text or "").strip()

        return await asyncio.to_thread(_call)
