import pytest
import httpx

BASE_URL = "http://127.0.0.1:8001"

TEST_USER = {"email": "test@gmail.com", "password": "test"}


@pytest.mark.asyncio
async def test_signup_success():
    #first signup should be successful
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/auth/signup", json=TEST_USER)

        assert response.status_code in (200, 201)

        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_signup_duplicate():
    #duplicate signup after the first should fail
    async with httpx.AsyncClient() as client:
 
        await client.post(f"{BASE_URL}/auth/signup", json=TEST_USER)

        response = await client.post(f"{BASE_URL}/auth/signup", json=TEST_USER)

        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_login_success():
    #signup then login should give access token
    async with httpx.AsyncClient() as client:

        await client.post(f"{BASE_URL}/auth/signup", json=TEST_USER)

        form_data = {"username": TEST_USER["email"], "password": TEST_USER["password"]}
        response = await client.post(f"{BASE_URL}/auth/login", data=form_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid():
    #invalid login should respond as such
    async with httpx.AsyncClient() as client:
        form_data = {"username": "wrong@example.com", "password": "wrongpass"}
        response = await client.post(f"{BASE_URL}/auth/login", data=form_data)

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"