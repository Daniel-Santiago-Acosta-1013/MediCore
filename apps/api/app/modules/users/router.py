from fastapi import APIRouter, Depends
from psycopg import Connection
from typing import List
from app.core.database import get_db
from app.core.permissions import get_current_user, require_role, UserRole
from app.modules.users.schemas import UserCreate, UserUpdate, UserOut
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserOut])
def list_users(
    limit: int = 100,
    offset: int = 0,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.RECEPTIONIST)),
):
    repo = UserRepository(conn)
    service = UserService(repo)
    return service.list_users(limit, offset)


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.RECEPTIONIST)),
):
    repo = UserRepository(conn)
    service = UserService(repo)
    return service.get_user(user_id)


@router.post("", response_model=UserOut)
def create_user(
    data: UserCreate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = UserRepository(conn)
    service = UserService(repo)
    return service.create_user(data)


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: str,
    data: UserUpdate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = UserRepository(conn)
    service = UserService(repo)
    return service.update_user(user_id, data)


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = UserRepository(conn)
    service = UserService(repo)
    return service.delete_user(user_id)
