from psycopg import Connection
from typing import Optional, Dict, Any


class AuthRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, email, password_hash, full_name, role, is_active, created_at, updated_at FROM users WHERE email = %s",
                (email,),
            )
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, email, password_hash, full_name, role, is_active, created_at, updated_at FROM users WHERE id = %s",
                (user_id,),
            )
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def create_user(self, email: str, password_hash: str, full_name: str, role: str) -> Dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (email, password_hash, full_name, role)
                VALUES (%s, %s, %s, %s)
                RETURNING id, email, full_name, role, is_active, created_at, updated_at
                """,
                (email, password_hash, full_name, role),
            )
            row = cur.fetchone()
            self.conn.commit()
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))
