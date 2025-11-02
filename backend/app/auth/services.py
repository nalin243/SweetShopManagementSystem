from app.core.config import settings
from app.users import services as user_services
from app import utils
from app.models import UserModel

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def authenticate_user(email: str, password: str) -> Optional[UserModel]:
    user = await user_services.get_user_by_email(email)
    if not user:
        return None
    if not utils.verify_password(password, user.password):
        return None
        
    return user



async def get_current_user(
    token: str = Depends(oauth2_scheme)
    ) -> Optional[UserModel]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_services.get_user_by_email(email)
    if user is None:
        raise credentials_exception

    return user



async def require_admin(
    current_user = Depends(get_current_user)
    ):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    return current_user