-- Revert medicore:audit_logs from pg

BEGIN;

DROP INDEX IF EXISTS idx_audit_logs_created_at;
DROP INDEX IF EXISTS idx_audit_logs_performed_by;
DROP INDEX IF EXISTS idx_audit_logs_record_id;
DROP INDEX IF EXISTS idx_audit_logs_table_name;
DROP TABLE IF EXISTS audit_logs;

COMMIT;
