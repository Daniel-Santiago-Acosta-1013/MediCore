-- Revert medicore:patients from pg

BEGIN;

DROP INDEX IF EXISTS idx_patients_user_id;
DROP INDEX IF EXISTS idx_patients_document_id;
DROP TABLE IF EXISTS patients;

COMMIT;
