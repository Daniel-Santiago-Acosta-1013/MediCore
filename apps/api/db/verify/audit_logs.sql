-- Verify medicore:audit_logs on pg

BEGIN;

SELECT id, table_name, record_id, action, old_data, new_data, performed_by, created_at
FROM audit_logs
WHERE FALSE;

ROLLBACK;
