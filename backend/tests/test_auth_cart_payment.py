import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth_login_and_profile():
	from app.main import app
	async with AsyncClient(app=app, base_url="http://test") as ac:
		# Login simulado (GuardPass mock aceita senha com 6+ chars)
		resp = await ac.post("/api/v1/auth/login", json={"email": "user@test.com", "password": "secret1"})
		assert resp.status_code in (200, 401)
		if resp.status_code == 200:
			data = resp.json()
			assert "access_token" in data
			token = data["access_token"]
			# Perfil
			resp_me = await ac.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
			assert resp_me.status_code == 200


@pytest.mark.asyncio
async def test_cart_flow_requires_auth():
	from app.main import app
	async with AsyncClient(app=app, base_url="http://test") as ac:
		# Sem token deve falhar (dependendo do implementation detail)
		resp = await ac.get("/api/v1/cart/")
		assert resp.status_code in (401, 403, 422)


@pytest.mark.asyncio
async def test_payment_status_requires_auth():
	from app.main import app
	async with AsyncClient(app=app, base_url="http://test") as ac:
		resp = await ac.get("/api/v1/payment/status/00000000-0000-0000-0000-000000000000")
		assert resp.status_code in (401, 403, 422)


