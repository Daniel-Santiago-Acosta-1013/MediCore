-- Revert medicore:medical_orders from pg

BEGIN;

DROP INDEX IF EXISTS idx_medical_orders_status;
DROP INDEX IF EXISTS idx_medical_orders_doctor_id;
DROP INDEX IF EXISTS idx_medical_orders_medical_record_id;
DROP TABLE IF EXISTS medical_orders;

COMMIT;
