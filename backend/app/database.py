from app.core.config import settings

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

users_collection = db["users"]
sweets_collection = db["sweets"]