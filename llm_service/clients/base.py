"""Abstract base class for all LLM clients."""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Interface that all LLM clients must implement."""

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate a completion for the given prompt.

        Args:
            prompt: The user prompt sent to the model.

        Returns:
            A string containing the generated response.
        """
        raise NotImplementedError
