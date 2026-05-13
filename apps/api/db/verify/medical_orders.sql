-- Verify medicore:medical_orders on pg

BEGIN;

SELECT id, medical_record_id, doctor_id, order_type, description, status, created_at, updated_at
FROM medical_orders
WHERE FALSE;

ROLLBACK;
