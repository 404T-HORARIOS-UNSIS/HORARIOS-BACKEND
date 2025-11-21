import uuid

import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_register_login_me():
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "testpass123"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Registrar
        r = await ac.post(
            "/auth/register",
            json={
                "username": username,
                "email": f"{username}@example.com",
                "password": password,
                "role": "SECRETARIA",
            },
        )
        assert r.status_code == 201, f"register failed: {r.status_code} {r.text}"

        # Login (form)
        r2 = await ac.post("/auth/login", data={"username": username, "password": password})
        assert r2.status_code == 200, f"login failed: {r2.status_code} {r2.text}"
        body = r2.json()
        assert "access_token" in body

        token = body["access_token"]

        # Me
        r3 = await ac.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r3.status_code == 200, f"me failed: {r3.status_code} {r3.text}"
        me = r3.json()
        assert me["username"] == username
