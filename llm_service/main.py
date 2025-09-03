"""Entry point for the FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status

from llm_service.manager import LLMClientFactory
from llm_service.models import GenerateResponse, GenerateRequest

app = FastAPI(
    title="LLM Client Manager",
    description="A simple API that routes prompts to different LLM providers",
    version="0.1.0",
)


@app.post(
    "/generate",
    response_model=GenerateResponse,
    summary="Generate text from the specified LLM client",
    response_description="The generated response from the LLM",
)
async def generate(request: GenerateRequest) -> GenerateResponse:
    """Handle a request to generate text from an LLM.

    Args:
        request: A request containing the prompt and the name of the client.

    Returns:
        A JSON response with the generated text.

    Raises:
        HTTPException: If the client is not registered or an error occurs during generation.
    """
    try:
        print(f"{request.client_name} is registered")
        client = LLMClientFactory.get_client(request.client_name)
    except ValueError as exc:
        # Client not found or invalid name
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    try:
        result = await client.generate(request.prompt)
    except Exception as exc:
        # Wrap any error from the client into a 500 response
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    return GenerateResponse(response=result)
