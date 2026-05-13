-- Revert medicore:medical_records from pg

BEGIN;

DROP INDEX IF EXISTS idx_medical_records_appointment_id;
DROP INDEX IF EXISTS idx_medical_records_doctor_id;
DROP INDEX IF EXISTS idx_medical_records_patient_id;
DROP TABLE IF EXISTS medical_records;

COMMIT;
