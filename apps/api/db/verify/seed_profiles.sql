-- Verify medicore:seed_profiles on pg

BEGIN;

SELECT 1/COUNT(*)::int
FROM doctors
WHERE user_id IN (
    SELECT id FROM users
    WHERE role = 'DOCTOR'
      AND email LIKE '%@medicore.com'
);

SELECT 1/COUNT(*)::int
FROM patients
WHERE user_id IN (
    SELECT id FROM users
    WHERE role = 'PATIENT'
      AND email LIKE '%@medicore.com'
);

ROLLBACK;
