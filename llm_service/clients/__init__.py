"""LLM clients package.

This package provides base and built-in client implementations.
Optional clients (OpenAI, Gemini, Claude) are not imported here to avoid
hard dependencies on their SDKs. They should be imported explicitly where needed.
"""

from .base import LLMClient  # noqa: F401
from .dummy import DummyClient  # noqa: F401
