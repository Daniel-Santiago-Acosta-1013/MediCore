-- Verify medicore:doctors on pg

BEGIN;

SELECT id, user_id, license_number, specialty, phone, created_at, updated_at
FROM doctors
WHERE FALSE;

ROLLBACK;
