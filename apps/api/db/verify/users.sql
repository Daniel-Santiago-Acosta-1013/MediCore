-- Verify medicore:users on pg

BEGIN;

SELECT id, email, password_hash, full_name, role, is_active, created_at, updated_at
FROM users
WHERE FALSE;

ROLLBACK;
