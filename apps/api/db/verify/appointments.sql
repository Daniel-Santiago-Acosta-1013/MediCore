-- Verify medicore:appointments on pg

BEGIN;

SELECT id, patient_id, doctor_id, appointment_date, status, notes, created_at, updated_at
FROM appointments
WHERE FALSE;

ROLLBACK;
