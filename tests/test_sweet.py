import pytest
import httpx

BASE_URL = "http://127.0.0.1:8001"

TEST_USER = {"email": "test@gmail.com", "password": "test"}
ADMIN_USER = {"email": "admin@gmail.com", "password": "admin"}

SWEET_DATA = {
    "name": "Boondi Ladoo",
    "category": "Traditional",
    "price": 50,
    "quantity": 10
}


async def get_token(email, password):
    #helper function for login and getting token
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/auth/signup", json={"email": email, "password": password})
        form = {"username": email, "password": password}
        res = await client.post(f"{BASE_URL}/auth/login", data=form)
        return res.json()["access_token"]


@pytest.mark.asyncio
async def test_add_sweet():
    #successful adding of sweet should return name and price
    token = await get_token(TEST_USER["email"], TEST_USER["password"])
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/api/sweets", json=SWEET_DATA, headers=headers)

        assert res.status_code in (200, 201)
        data = res.json()
        assert data["name"] == SWEET_DATA["name"]
        assert data["price"] == SWEET_DATA["price"]


@pytest.mark.asyncio
async def test_get_all_sweets():
    #get list of sweets, previously inserted sweet should be present
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/api/sweets")

        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert any(sweet["name"] == "Ladoo" for sweet in data)


@pytest.mark.asyncio
async def test_search_sweets_by_name():
    #get sweet by name
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/api/sweets/search", params={"name": "Ladoo"})

        assert res.status_code == 200
        results = res.json()
        assert len(results) >= 1
        assert any("Ladoo" in sweet["name"] for sweet in results)


@pytest.mark.asyncio
async def test_update_sweet():
    #update details for sweet
    token = await get_token(TEST_USER["email"], TEST_USER["password"])
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"name": "Motichoor Ladoo", "price": 60, "category": "Traditional", "quantity": 15}

    async with httpx.AsyncClient() as client:
        res = await client.put(f"{BASE_URL}/api/sweets/s1", json=update_data, headers=headers)

        assert res.status_code == 200
        updated = res.json()
        assert updated["name"] == "Motichoor Ladoo"
        assert updated["price"] == 60


@pytest.mark.asyncio
async def test_delete_sweet_admin_only():
    #successful deletion of sweet
    admin_token = await get_token(ADMIN_USER["email"], ADMIN_USER["password"])
    headers = {"Authorization": f"Bearer {admin_token}"}

    async with httpx.AsyncClient() as client:
        res = await client.delete(f"{BASE_URL}/api/sweets/s1", headers=headers)

        assert res.status_code in (200, 204)

        # Verify deletion
        verify = await client.get(f"{BASE_URL}/api/sweets/search", params={"name": "Motichoor"})
        assert verify.status_code == 200
        assert len(verify.json()) == 0
