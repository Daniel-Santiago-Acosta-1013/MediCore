-- Revert medicore:invoices from pg

BEGIN;

DROP INDEX IF EXISTS idx_invoices_due_date;
DROP INDEX IF EXISTS idx_invoices_status;
DROP INDEX IF EXISTS idx_invoices_patient_id;
DROP TABLE IF EXISTS invoices;

COMMIT;
