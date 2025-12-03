import uuid

import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.asyncio
async def test_register_login_me():
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "testpass123"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post(
            "/auth/register",
            json={
                "username": username,
                "email": f"{username}@example.com",
                "password": password,
                "role": "SECRETARIA",
            },
        )
        assert r.status_code in (201, 409)

        r2 = await ac.post("/auth/login", data={"username": username, "password": password})
        assert r2.status_code == 200
        body = r2.json()
        token = body["access_token"]

        r3 = await ac.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r3.status_code == 200
        me = r3.json()
        assert me["username"] == username
        assert me["role"] == "SECRETARIA"
