from app.schemas import Token, UserCreate
from app import utils
from app.users import services as user_services
from app.auth import services as auth_services
from app.core.config import settings

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
async def signup(user_create: UserCreate):
    pass

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass