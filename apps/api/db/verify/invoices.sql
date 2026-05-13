-- Verify medicore:invoices on pg

BEGIN;

SELECT id, patient_id, appointment_id, amount, status, due_date, paid_at, created_at, updated_at
FROM invoices
WHERE FALSE;

ROLLBACK;
