-- Verify medicore:patients on pg

BEGIN;

SELECT id, user_id, document_id, date_of_birth, phone, address, emergency_contact_name, emergency_contact_phone, created_at, updated_at
FROM patients
WHERE FALSE;

ROLLBACK;
