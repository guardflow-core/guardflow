import pytest
from httpx import AsyncClient
from fastapi import FastAPI


@pytest.mark.asyncio
async def test_health_endpoint():
	from app.main import app  # import inside to ensure app is initialized
	assert isinstance(app, FastAPI)
	async with AsyncClient(app=app, base_url="http://test") as ac:
		resp = await ac.get("/health")
		assert resp.status_code == 200
		data = resp.json()
		assert data.get("status") == "healthy"
		assert "version" in data
		assert "environment" in data



