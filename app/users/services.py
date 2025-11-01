from fastapi import HTTPException
from app.database import users_collection
from app.models import UserModel
from app import utils

from typing import Optional
from bson import ObjectId

async def get_user_by_email(email: str) -> Optional[UserModel]:
    doc = await users_collection.find_one({"email": email})
    if doc:
        doc["id"] = doc.get("_id")
        return UserModel(**doc)
    return None

async def get_user_by_id(user_id: str) -> Optional[UserModel]:
    if not ObjectId.is_valid(user_id):
        return None
    doc = await users_collection.find_one({"_id": ObjectId(user_id)})
    if doc:
        doc["id"] = doc.get("_id")
        return UserModel(**doc)
    return None

async def create_user(email: str, password: str, role:str="user") -> UserModel:
    hashed_pw = utils.hash_password(password)
    user_doc = {"email": email, "password": hashed_pw, "role":role}
    result = await users_collection.insert_one(user_doc)
    new_doc = await users_collection.find_one({"_id": result.inserted_id})
    new_doc["id"] = new_doc.get("_id")
    return UserModel(**new_doc)

async def promote_user(email: str):
    user = await users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found"
            )
    await users_collection.update_one({"email": email}, {"$set": {"role": "admin"}})
    return {"message": "User promoted"}

