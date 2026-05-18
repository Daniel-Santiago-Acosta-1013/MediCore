-- Revert medicore:seed_users from pg

BEGIN;

DELETE FROM users WHERE email LIKE '%@medicore.com';

COMMIT;
