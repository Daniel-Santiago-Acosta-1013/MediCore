from fastapi import HTTPException, status
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def list_users(self, limit: int = 100, offset: int = 0):
        return self.repo.list_users(limit, offset)

    def get_user(self, user_id: str):
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def create_user(self, data: UserCreate):
        from app.modules.auth.repository import AuthRepository
        auth_repo = AuthRepository(self.repo.conn)
        existing = auth_repo.get_user_by_email(data.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        password_hash = get_password_hash(data.password)
        with self.repo.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (email, password_hash, full_name, role, is_active)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, email, full_name, role, is_active, created_at, updated_at
                """,
                (data.email, password_hash, data.full_name, data.role.upper(), data.is_active),
            )
            row = cur.fetchone()
            self.repo.conn.commit()
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))

    def update_user(self, user_id: str, data: UserUpdate):
        update_data = data.model_dump(exclude_unset=True)
        user = self.repo.update_user(user_id, update_data)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def delete_user(self, user_id: str):
        deleted = self.repo.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"detail": "User deleted"}
