from psycopg import Connection
from typing import Optional, Dict, Any, List


class PatientRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def list_patients(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, user_id, document_id, date_of_birth, phone, address, emergency_contact_name, emergency_contact_phone, created_at, updated_at FROM patients ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, offset),
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_patient_by_id(self, patient_id: str) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, user_id, document_id, date_of_birth, phone, address, emergency_contact_name, emergency_contact_phone, created_at, updated_at FROM patients WHERE id = %s",
                (patient_id,),
            )
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def create_patient(self, data: Dict[str, Any]) -> Dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO patients (user_id, document_id, date_of_birth, phone, address, emergency_contact_name, emergency_contact_phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, user_id, document_id, date_of_birth, phone, address, emergency_contact_name, emergency_contact_phone, created_at, updated_at
                """,
                (data.get("user_id"), data["document_id"], data.get("date_of_birth"), data.get("phone"), data.get("address"), data.get("emergency_contact_name"), data.get("emergency_contact_phone")),
            )
            row = cur.fetchone()
            self.conn.commit()
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))

    def update_patient(self, patient_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            fields = []
            values = []
            for key, value in data.items():
                if value is not None:
                    fields.append(f"{key} = %s")
                    values.append(value)
            if not fields:
                return self.get_patient_by_id(patient_id)
            values.append(patient_id)
            query = f"UPDATE patients SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING id, user_id, document_id, date_of_birth, phone, address, emergency_contact_name, emergency_contact_phone, created_at, updated_at"
            cur.execute(query, tuple(values))
            row = cur.fetchone()
            self.conn.commit()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def delete_patient(self, patient_id: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
            self.conn.commit()
            return cur.rowcount > 0
