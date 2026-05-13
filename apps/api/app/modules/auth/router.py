from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from psycopg import Connection
from app.core.database import get_db
from app.core.permissions import get_current_user
from app.modules.auth.schemas import UserRegister, Token, UserOut
from app.modules.auth.repository import AuthRepository
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(data: UserRegister, conn: Connection = Depends(get_db)):
    repo = AuthRepository(conn)
    service = AuthService(repo)
    return service.register(data)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), conn: Connection = Depends(get_db)):
    repo = AuthRepository(conn)
    service = AuthService(repo)
    return service.login(form_data.username, form_data.password)


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    current_user.pop("password_hash", None)
    return current_user
