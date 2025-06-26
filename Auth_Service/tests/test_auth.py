import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register
        resp = await ac.post("/auth/register", json={
            "email": "test@example.com",
            "password": "secret123",
            "role": "user"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "test@example.com"

        # Login
        resp = await ac.post("/auth/login", json={
            "email": "test@example.com",
            "password": "secret123"
        })
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        assert token
