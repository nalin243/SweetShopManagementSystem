from bson import int64
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role:str = "user"

class UserOut(BaseModel):
    id: str
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SweetRequest(BaseModel):
    name: str
    category: str
    price: int
    quantity: int

class SweetResponse(BaseModel):
    name: str
    category: str
    price: int
    quantity: int