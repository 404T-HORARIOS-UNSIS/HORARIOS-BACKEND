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

        import pytest
        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)

        @pytest.mark.parametrize("username,email,password,role", [
            ("user_test_api", "user_test_api@example.com", "Pass1234", "SECRETARIA"),
        ])
        def test_auth_flow(username, email, password, role):
            r = client.post("/auth/register", json={
                "username": username,
                "email": email,
                "password": password,
                "role": role,
            })
            assert r.status_code in (200, 201, 409)

            r = client.post(
                "/auth/login",
                data={"username": username, "password": password},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            assert r.status_code == 200
            token = r.json()["access_token"]

            r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
            assert r.status_code == 200
            body = r.json()
            assert body["username"] == username
            assert body["role"] == role
