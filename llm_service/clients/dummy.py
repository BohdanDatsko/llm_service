"""A simple dummy LLM client used for testing and fallback purposes."""

from __future__ import annotations

from .base import LLMClient


class DummyClient(LLMClient):
    """A basic LLM client that echoes the prompt back to the caller."""

    async def generate(self, prompt: str) -> str:
        """Return a trivial response for testing.

        This client simply prefixes the user's prompt with ``"Echo: "``. In a real
        implementation you might call a model hosted on your own infrastructure or
        a publicly available endpoint.
        """
        return f"Echo: {prompt}"