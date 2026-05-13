-- Revert medicore:doctors from pg

BEGIN;

DROP INDEX IF EXISTS idx_doctors_user_id;
DROP INDEX IF EXISTS idx_doctors_license_number;
DROP TABLE IF EXISTS doctors;

COMMIT;
