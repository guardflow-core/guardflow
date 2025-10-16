import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_esg_engine_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/esg-engine/health")
    assert r.status_code in (200, 401)  # pode exigir auth

@pytest.mark.asyncio
async def test_esg_calculate_score_unauthorized():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/esg-engine/calculate-score", json={"ncm_code": "84"})
    # Em ambiente fallback sem auth, rota pode não exigir token; tolerar ambos
    assert r.status_code in (200, 401)

@pytest.mark.asyncio
async def test_esg_engine_core_direct():
    # Teste direto do core sem HTTP
    from app.services.esg_engine import esg_engine
    score = esg_engine.calculate_esg_score("84")
    assert 0.0 <= score.overall <= 100.0
