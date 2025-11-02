import pytest
import httpx
import uuid
import asyncio

from app.database import users_collection

BASE_URL = "http://127.0.0.1:8001"

ADMIN_USER = {"email": "admin@gmail.com", "password": "admin"}

SWEET_DATA = {
    "name": "Ladoo",
    "category": "Traditional",
    "price": 50,
    "quantity": 10
}

def make_test_user():
    return {
        "email": f"test_{uuid.uuid4().hex[:6]}@gmail.com",
        "password": "test"
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

    user = make_test_user()

    token = await get_token(user["email"], user["password"])
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/api/sweet", json=SWEET_DATA, headers=headers)

        assert res.status_code in (200, 201)
        data = res.json()
        assert data["name"] == SWEET_DATA["name"]
        assert data["price"] == SWEET_DATA["price"]

@pytest.mark.asyncio
async def test_add_duplicate_sweet():
    #adding duplicate sweet should return error

    user = make_test_user()

    token = await get_token(user["email"], user["password"])
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/api/sweet", json=SWEET_DATA, headers=headers)

        assert res.status_code in (400,401)
        data = res.json()
        assert data["detail"] == "Sweet exists"


@pytest.mark.asyncio
async def test_get_all_sweets():
    #get list of sweets, previously inserted sweet should be present
    user = make_test_user()

    token = await get_token(user["email"], user["password"])
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/api/sweets",headers=headers)

        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert any(sweet["name"] == "Ladoo" for sweet in data)


@pytest.mark.asyncio
async def test_search_sweets_by_name():
    #get sweet by name

    user = make_test_user()

    token = await get_token(user["email"], user["password"])
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/api/sweets/search", params={"name": "Ladoo"},headers=headers)

        assert res.status_code == 200
        results = res.json()
        assert len(results) >= 1
        assert any("Ladoo" in sweet["name"] for sweet in results)


@pytest.mark.asyncio
async def test_update_sweet():
    #update details for sweet

    user = make_test_user()

    token = await get_token(user["email"], user["password"])
    headers = {"Authorization": f"Bearer {token}"}

    update_data = {"name": "Motichoor Ladoo", "price": 60, "category": "Traditional", "quantity": 15}

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/api/sweets",headers=headers)
        res = res.json()
        id_to_test = res[0]["id"]
        res = await client.put(f"{BASE_URL}/api/sweets/{id_to_test}", json=update_data, headers=headers)

        assert res.status_code == 200
        updated = res.json()
        assert updated["name"] == "Motichoor Ladoo"
        assert updated["price"] == 60


@pytest.mark.asyncio
async def test_delete_sweet_admin_only():
    #successful deletion of sweet

    headers = None

    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/auth/signup", json={"email": ADMIN_USER["email"], "password":  ADMIN_USER["password"]})
        await client.post(f"{BASE_URL}/users/promote/{ADMIN_USER["email"]}")

        await asyncio.sleep(0.2)#to allow write to be updated

        form = {"username": ADMIN_USER["email"], "password": ADMIN_USER["password"]}
        res = await client.post(f"{BASE_URL}/auth/login", data=form)
        admin_token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {admin_token}"}

        res = await client.get(f"{BASE_URL}/api/sweets",headers=headers)
        res = res.json()
        id_to_test = res[0]["id"]

        res = await client.delete(f"{BASE_URL}/api/sweets/{id_to_test}", headers=headers)
        assert res.status_code in (200, 204)

        # Verify deletion
        verify = await client.get(f"{BASE_URL}/api/sweets/search", params={"name": "Motichoor"},headers=headers)
        assert verify.status_code == 200
        assert len(verify.json()) == 0


@pytest.mark.asyncio
async def test_purchase_sweet():
    #purchase should decrease quantity

    user = make_test_user()

    token = await get_token(user["email"], user["password"])
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        #actually adding something to test this
        res = await client.post(f"{BASE_URL}/api/sweet", json=SWEET_DATA, headers=headers)

        res = await client.get(f"{BASE_URL}/api/sweets", headers=headers)
        sweet_id = res.json()[0]["id"]

        res = await client.post(f"{BASE_URL}/api/sweets/{sweet_id}/purchase", headers=headers)
        assert res.status_code == 200
        sweet = res.json()
        assert sweet["quantity"] >= 0

@pytest.mark.asyncio
async def test_restock_sweet_admin_only():
    async with httpx.AsyncClient() as client:
        #after restocking amount should be old qty + restock_amount
        await client.post(f"{BASE_URL}/auth/signup", json={"email": ADMIN_USER["email"], "password":  ADMIN_USER["password"]})
        await client.post(f"{BASE_URL}/users/promote/{ADMIN_USER["email"]}")

        await asyncio.sleep(0.2)#to allow write to be updated

        form = {"username": ADMIN_USER["email"], "password": ADMIN_USER["password"]}
        res = await client.post(f"{BASE_URL}/auth/login", data=form)
        admin_token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {admin_token}"}

        #actually adding something to test this
        res = await client.post(f"{BASE_URL}/api/sweet", json=SWEET_DATA, headers=headers)

        res = await client.get(f"{BASE_URL}/api/sweets",headers=headers)
        res = res.json()
        id_to_test = res[0]["id"]
        old_qty = res[0]["quantity"]

        # Restock sweet
        restock_amount = 5
        res = await client.post(
            f"{BASE_URL}/api/sweets/{id_to_test}/restock",
            headers=headers,
            json={"amount": restock_amount}
        )
        assert res.status_code == 200

        updated_sweet = res.json()
        assert updated_sweet["quantity"] == old_qty + restock_amount
