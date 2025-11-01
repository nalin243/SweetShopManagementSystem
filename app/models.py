from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId
from pydantic import field_validator  # optional for v2 features

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class UserModel(BaseModel):
    id: Optional[PyObjectId] = None
    email: EmailStr
    password: str

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True