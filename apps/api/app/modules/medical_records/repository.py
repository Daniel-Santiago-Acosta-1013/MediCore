from psycopg import Connection
from typing import Optional, Dict, Any, List


class MedicalRecordRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def list_records(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, patient_id, doctor_id, appointment_id, diagnosis, treatment, notes, created_at, updated_at FROM medical_records ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, offset),
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_record_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, patient_id, doctor_id, appointment_id, diagnosis, treatment, notes, created_at, updated_at FROM medical_records WHERE id = %s",
                (record_id,),
            )
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def create_record(self, data: Dict[str, Any]) -> Dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO medical_records (patient_id, doctor_id, appointment_id, diagnosis, treatment, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, patient_id, doctor_id, appointment_id, diagnosis, treatment, notes, created_at, updated_at
                """,
                (data["patient_id"], data.get("doctor_id"), data.get("appointment_id"), data["diagnosis"], data.get("treatment"), data.get("notes")),
            )
            row = cur.fetchone()
            self.conn.commit()
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))

    def update_record(self, record_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            fields = []
            values = []
            for key, value in data.items():
                if value is not None:
                    fields.append(f"{key} = %s")
                    values.append(value)
            if not fields:
                return self.get_record_by_id(record_id)
            values.append(record_id)
            query = f"UPDATE medical_records SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING id, patient_id, doctor_id, appointment_id, diagnosis, treatment, notes, created_at, updated_at"
            cur.execute(query, tuple(values))
            row = cur.fetchone()
            self.conn.commit()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def delete_record(self, record_id: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM medical_records WHERE id = %s", (record_id,))
            self.conn.commit()
            return cur.rowcount > 0
