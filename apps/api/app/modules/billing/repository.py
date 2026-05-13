from psycopg import Connection
from typing import Optional, Dict, Any, List


class InvoiceRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def list_invoices(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, patient_id, appointment_id, amount, status, due_date, paid_at, created_at, updated_at FROM invoices ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, offset),
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_invoice_by_id(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, patient_id, appointment_id, amount, status, due_date, paid_at, created_at, updated_at FROM invoices WHERE id = %s",
                (invoice_id,),
            )
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def create_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO invoices (patient_id, appointment_id, amount, status, due_date, paid_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, patient_id, appointment_id, amount, status, due_date, paid_at, created_at, updated_at
                """,
                (data["patient_id"], data.get("appointment_id"), data["amount"], data.get("status", "PENDING"), data.get("due_date"), data.get("paid_at")),
            )
            row = cur.fetchone()
            self.conn.commit()
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))

    def update_invoice(self, invoice_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cur:
            fields = []
            values = []
            for key, value in data.items():
                if value is not None:
                    fields.append(f"{key} = %s")
                    values.append(value)
            if not fields:
                return self.get_invoice_by_id(invoice_id)
            values.append(invoice_id)
            query = f"UPDATE invoices SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING id, patient_id, appointment_id, amount, status, due_date, paid_at, created_at, updated_at"
            cur.execute(query, tuple(values))
            row = cur.fetchone()
            self.conn.commit()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

    def delete_invoice(self, invoice_id: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM invoices WHERE id = %s", (invoice_id,))
            self.conn.commit()
            return cur.rowcount > 0
