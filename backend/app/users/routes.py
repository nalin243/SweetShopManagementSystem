from app.schemas import UserOut
from app.auth import services as auth_services
from app.users import services as user_services

from fastapi import APIRouter, Depends,Path

router = APIRouter(prefix="/users", tags=["users"])

#only for development and testing
@router.post("/promote/{email}")
async def promote_user(email: str = Path(..., description="email of user to be promoted")):
    return await user_services.promote_user(email=email)
