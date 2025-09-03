"""Pydantic request and response models for the API."""

from __future__ import annotations

from pydantic import BaseModel, Field, AliasChoices, ConfigDict


class GenerateRequest(BaseModel):
    """Model for the /generate request body."""

    prompt: str = Field(..., description="The prompt to send to the language model")
    client_name: str = Field(
        ...,
        validation_alias=AliasChoices("client_name", "clientName"),
        serialization_alias="clientName",
        description="The client to use (e.g., dummy, openai)",
    )
    model_config = ConfigDict(populate_by_name=True)


class GenerateResponse(BaseModel):
    """Model for the /generate response body."""

    response: str = Field(..., description="The generated text returned by the LLM")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "response": "Hello! How can I assist you today?",
                }
            ]
        }
