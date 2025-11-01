from app.schemas import UserOut
from app.auth import services as auth_services

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
async def read_me(current_user = Depends(auth_services.get_current_user)):
    pass