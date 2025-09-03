"""Client manager that returns the appropriate LLM client by name."""

from __future__ import annotations

from typing import Callable, Dict

from llm_service.clients import LLMClient, DummyClient

# Optional clients — register only if import succeeds
OpenAIClient = None
GeminiClient = None
ClaudeClient = None
try:
    from llm_service.clients.openai_client import OpenAIClient as _OpenAIClient  # type: ignore

    OpenAIClient = _OpenAIClient
except Exception:
    OpenAIClient = None

try:
    from llm_service.clients.gemini_client import GeminiClient as _GeminiClient  # type: ignore

    GeminiClient = _GeminiClient
except Exception:
    GeminiClient = None

try:
    from llm_service.clients.claude_client import ClaudeClient as _ClaudeClient  # type: ignore

    ClaudeClient = _ClaudeClient
except Exception:
    ClaudeClient = None


class LLMClientFactory:
    """Simple Factory: name -> provider callable returning an `LLMClient`."""
    _clients: Dict[str, Callable[[], LLMClient]] = {
        "dummy": DummyClient,
    }
    if OpenAIClient:
        _clients["openai"] = lambda: OpenAIClient()  # type: ignore[misc,call-arg]
    if GeminiClient:
        _clients["gemini"] = lambda: GeminiClient()  # type: ignore[misc,call-arg]
    if ClaudeClient:
        _clients["claude"] = lambda: ClaudeClient()  # type: ignore[misc,call-arg]

    @classmethod
    def register(cls, name: str, provider: Callable[[], LLMClient]) -> None:
        """Register a new client provider at runtime.

        Args:
            name: Public name used by API callers (case-insensitive).
            provider: Zero-argument callable returning an `LLMClient` instance.
        """
        key = name.strip().lower()
        if not key:
            raise ValueError("Client name must be non-empty.")
        cls._clients[key] = provider

    @classmethod
    def get_client(cls, name: str) -> LLMClient:
        """Return an instance of the requested client.

        Raises:
            ValueError: If the client name is empty or not registered.
        """
        if not name:
            raise ValueError("client_name must be provided")

        key = name.strip().lower()
        provider = cls._clients.get(key)
        if not provider:
            raise ValueError(f"LLM client '{name}' is not registered")

        return provider()
