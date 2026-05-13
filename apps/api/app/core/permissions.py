from enum import Enum
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"
    RECEPTIONIST = "RECEPTIONIST"
    BILLING = "BILLING"
    PATIENT = "PATIENT"


def get_current_user(token: str = Depends(oauth2_scheme), conn=Depends(get_db)):
    from app.modules.auth.repository import AuthRepository

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    repo = AuthRepository(conn)
    user = repo.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


def require_role(*roles: UserRole):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user["role"] not in [r.value for r in roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user
    return role_checker
