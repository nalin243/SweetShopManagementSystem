import asyncio
from app.database import users_collection

async def make_admin(email):
    res = await users_collection.update_one({"email": email}, {"$set": {"role": "admin"}})
    print("✅ Admin set!" if res.modified_count else "⚠️ User not found")

if __name__ == "__main__":
    import sys
    email = sys.argv[1]
    asyncio.run(make_admin(email))
