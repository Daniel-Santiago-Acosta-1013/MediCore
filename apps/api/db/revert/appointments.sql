-- Revert medicore:appointments from pg

BEGIN;

DROP INDEX IF EXISTS idx_appointments_status;
DROP INDEX IF EXISTS idx_appointments_appointment_date;
DROP INDEX IF EXISTS idx_appointments_doctor_id;
DROP INDEX IF EXISTS idx_appointments_patient_id;
DROP TABLE IF EXISTS appointments;

COMMIT;
