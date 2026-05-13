from psycopg import Connection
from typing import Optional, Dict, Any, List


class MedicalOrderRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def list_orders(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, medical_record_id, doctor_id, order_type, description, status, created_at, updated_at FROM medical_orders ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, offset),
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_order_by_id(self, order_id: str) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, medical_record_id, doctor_id, order_type, description, status, created_at, updated_at FROM medical_orders WHERE id = %s",
                (order_id,),
            )
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def create_order(self, data: Dict[str, Any]) -> Dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO medical_orders (medical_record_id, doctor_id, order_type, description, status)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, medical_record_id, doctor_id, order_type, description, status, created_at, updated_at
                """,
                (data["medical_record_id"], data.get("doctor_id"), data["order_type"], data["description"], data.get("status", "PENDING")),
            )
            row = cur.fetchone()
            self.conn.commit()
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))

    def update_order(self, order_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            fields = []
            values = []
            for key, value in data.items():
                if value is not None:
                    fields.append(f"{key} = %s")
                    values.append(value)
            if not fields:
                return self.get_order_by_id(order_id)
            values.append(order_id)
            query = f"UPDATE medical_orders SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING id, medical_record_id, doctor_id, order_type, description, status, created_at, updated_at"
            cur.execute(query, tuple(values))
            row = cur.fetchone()
            self.conn.commit()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def delete_order(self, order_id: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM medical_orders WHERE id = %s", (order_id,))
            self.conn.commit()
            return cur.rowcount > 0
