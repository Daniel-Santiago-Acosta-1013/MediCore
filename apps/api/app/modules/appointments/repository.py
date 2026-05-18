from psycopg import Connection
from typing import Optional, Dict, Any, List


class AppointmentRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def _appointment_columns(self) -> str:
        return """
            a.id,
            a.patient_id,
            a.doctor_id,
            a.appointment_date,
            a.status,
            a.notes,
            a.created_at,
            a.updated_at,
            COALESCE(pu.full_name, 'Paciente') as patient_name,
            COALESCE(du.full_name, 'Doctor') as doctor_name
        """

    def _appointment_from(self) -> str:
        return """
            appointments a
            LEFT JOIN patients p ON p.id = a.patient_id
            LEFT JOIN users pu ON pu.id = p.user_id
            LEFT JOIN doctors d ON d.id = a.doctor_id
            LEFT JOIN users du ON du.id = d.user_id
        """

    def list_appointments(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT {self._appointment_columns()}
                FROM {self._appointment_from()}
                ORDER BY a.appointment_date DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_appointment_by_id(self, appointment_id: str) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT {self._appointment_columns()}
                FROM {self._appointment_from()}
                WHERE a.id = %s
                """,
                (appointment_id,),
            )
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def create_appointment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, patient_id, doctor_id, appointment_date, status, notes, created_at, updated_at
                """,
                (data["patient_id"], data["doctor_id"], data["appointment_date"], data.get("status", "SCHEDULED"), data.get("notes")),
            )
            row = cur.fetchone()
            self.conn.commit()
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))

    def update_appointment(self, appointment_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            fields = []
            values = []
            for key, value in data.items():
                if value is not None:
                    fields.append(f"{key} = %s")
                    values.append(value)
            if not fields:
                return self.get_appointment_by_id(appointment_id)
            values.append(appointment_id)
            query = f"UPDATE appointments SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING id, patient_id, doctor_id, appointment_date, status, notes, created_at, updated_at"
            cur.execute(query, tuple(values))
            row = cur.fetchone()
            self.conn.commit()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def delete_appointment(self, appointment_id: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
            self.conn.commit()
            return cur.rowcount > 0
