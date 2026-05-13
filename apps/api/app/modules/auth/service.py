from fastapi import HTTPException, status
from app.core.security import verify_password, get_password_hash, create_access_token
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import UserRegister


class AuthService:
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def register(self, data: UserRegister):
        existing = self.repo.get_user_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        password_hash = get_password_hash(data.password)
        user = self.repo.create_user(
            email=data.email,
            password_hash=password_hash,
            full_name=data.full_name,
            role=data.role.upper(),
        )
        return user

    def login(self, username: str, password: str):
        user = self.repo.get_user_by_email(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive",
            )
        if not verify_password(password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": str(user["id"])})
        return {"access_token": access_token, "token_type": "bearer"}

    def me(self, user_id: str):
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        user.pop("password_hash", None)
        return user
