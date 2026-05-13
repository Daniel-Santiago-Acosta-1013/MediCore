from psycopg import Connection
from typing import Optional, Dict, Any, List


class DoctorRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def list_doctors(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, user_id, license_number, specialty, phone, created_at, updated_at FROM doctors ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, offset),
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_doctor_by_id(self, doctor_id: str) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, user_id, license_number, specialty, phone, created_at, updated_at FROM doctors WHERE id = %s",
                (doctor_id,),
            )
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def create_doctor(self, data: Dict[str, Any]) -> Dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO doctors (user_id, license_number, specialty, phone)
                VALUES (%s, %s, %s, %s)
                RETURNING id, user_id, license_number, specialty, phone, created_at, updated_at
                """,
                (data["user_id"], data["license_number"], data["specialty"], data.get("phone")),
            )
            row = cur.fetchone()
            self.conn.commit()
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))

    def update_doctor(self, doctor_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            fields = []
            values = []
            for key, value in data.items():
                if value is not None:
                    fields.append(f"{key} = %s")
                    values.append(value)
            if not fields:
                return self.get_doctor_by_id(doctor_id)
            values.append(doctor_id)
            query = f"UPDATE doctors SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING id, user_id, license_number, specialty, phone, created_at, updated_at"
            cur.execute(query, tuple(values))
            row = cur.fetchone()
            self.conn.commit()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def delete_doctor(self, doctor_id: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
            self.conn.commit()
            return cur.rowcount > 0
