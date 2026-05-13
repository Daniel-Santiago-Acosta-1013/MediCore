-- Verify medicore:medical_records on pg

BEGIN;

SELECT id, patient_id, doctor_id, appointment_id, diagnosis, treatment, notes, created_at, updated_at
FROM medical_records
WHERE FALSE;

ROLLBACK;
