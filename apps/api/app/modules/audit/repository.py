from psycopg import Connection
from typing import Optional, Dict, Any, List
import json


class AuditRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def list_logs(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, table_name, record_id, action, old_data, new_data, performed_by, created_at FROM audit_logs ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, offset),
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_log_by_id(self, log_id: str) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, table_name, record_id, action, old_data, new_data, performed_by, created_at FROM audit_logs WHERE id = %s",
                (log_id,),
            )
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def create_log(self, data: Dict[str, Any]) -> Dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO audit_logs (table_name, record_id, action, old_data, new_data, performed_by)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, table_name, record_id, action, old_data, new_data, performed_by, created_at
                """,
                (
                    data["table_name"],
                    data["record_id"],
                    data["action"],
                    json.dumps(data["old_data"]) if data.get("old_data") else None,
                    json.dumps(data["new_data"]) if data.get("new_data") else None,
                    data.get("performed_by"),
                ),
            )
            row = cur.fetchone()
            self.conn.commit()
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))
