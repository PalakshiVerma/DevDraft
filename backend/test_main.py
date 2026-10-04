import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    # renamed from gemini_configured -> llm_configured
    assert "llm_configured" in data


@pytest.mark.asyncio
async def test_polish_endpoint_validation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Too short raw_text (min_length=5)
        response = await ac.post("/api/polish", json={"raw_text": "hi", "task_type": "standup"})
    assert response.status_code == 422
