import pytest
import httpx
import uuid

BASE_URL = "http://127.0.0.1:8001"

def make_test_user():
    return {
        "email": f"test_{uuid.uuid4().hex[:6]}@gmail.com",
        "password": "test"
    }


@pytest.mark.asyncio
async def test_signup_success():
    #first signup should be successful

    user = make_test_user()

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/auth/signup", json=user)

        assert response.status_code in (200, 201)

        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_signup_duplicate():
    #duplicate signup after the first should fail

    user = make_test_user()

    async with httpx.AsyncClient() as client:
 
        await client.post(f"{BASE_URL}/api/auth/signup", json=user)

        response = await client.post(f"{BASE_URL}/api/auth/signup", json=user)

        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_login_success():
    #signup then login should give access token

    user = make_test_user()

    async with httpx.AsyncClient() as client:

        await client.post(f"{BASE_URL}/api/auth/signup", json=user)

        form_data = {"username": user["email"], "password": user["password"]}
        response = await client.post(f"{BASE_URL}/api/auth/login", data=form_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid():
    #invalid login should respond as such

    user = make_test_user()

    async with httpx.AsyncClient() as client:
        form_data = {"username": "wrong@example.com", "password": "wrongpass"}
        response = await client.post(f"{BASE_URL}/api/auth/login", data=form_data)

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"