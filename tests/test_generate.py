import httpx
import pytest

from llm_service.main import app


@pytest.mark.asyncio
async def test_generate_with_dummy_client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/generate",
            json={"prompt": "hello", "clientName": "dummy"},
        )
    assert resp.status_code == 200
    assert resp.json() == {"response": "Echo: hello"}


@pytest.mark.asyncio
async def test_generate_with_unknown_client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/generate",
            json={"prompt": "x", "client_name": "nope"},
        )
    assert resp.status_code == 400
    data = resp.json()
    assert "detail" in data and "LLM client 'nope' is not registered" in data["detail"]
