-- Verify medicore:seed_users on pg

BEGIN;

SELECT 1/COUNT(*)::int FROM users WHERE email LIKE '%@medicore.com';

ROLLBACK;
