from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from app.schemas import Token, UserCreate
from app import utils
from app.users import services as user_services
from app.auth import services as auth_services
from app.core.config import settings
from app.core import security

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
async def signup(user_create: UserCreate):
    existing_user = await user_services.get_user_by_email(user_create.email)

    if existing_user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Email already registered"
            )
    else:
        new_user = await user_services.create_user(user_create.email,user_create.password)
        access_token = security.create_access_token({"sub":user_create.email})
        return {"access_token":access_token,"token_type":"bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    existing_user = await user_services.get_user_by_email(form_data.username)

    if(existing_user):
        user = await auth_services.authenticate_user(form_data.username,form_data.password)
        access_token = security.create_access_token({"sub":user.email})
        return {"access_token":access_token,"token_type":"bearer"}
    else:
        raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )