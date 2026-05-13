from psycopg import Connection
from typing import Optional, Dict, Any, List


class UserRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def list_users(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, email, full_name, role, is_active, created_at, updated_at FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, offset),
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, email, full_name, role, is_active, created_at, updated_at FROM users WHERE id = %s",
                (user_id,),
            )
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def update_user(self, user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            fields = []
            values = []
            for key, value in data.items():
                if value is not None:
                    fields.append(f"{key} = %s")
                    values.append(value)
            if not fields:
                return self.get_user_by_id(user_id)
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING id, email, full_name, role, is_active, created_at, updated_at"
            cur.execute(query, tuple(values))
            row = cur.fetchone()
            self.conn.commit()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def delete_user(self, user_id: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.conn.commit()
            return cur.rowcount > 0
