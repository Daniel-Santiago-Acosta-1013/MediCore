-- Revert medicore:seed_profiles from pg

BEGIN;

DELETE FROM doctors
WHERE user_id IN (
    SELECT id FROM users
    WHERE role = 'DOCTOR'
      AND email LIKE '%@medicore.com'
);

DELETE FROM patients
WHERE user_id IN (
    SELECT id FROM users
    WHERE role = 'PATIENT'
      AND email LIKE '%@medicore.com'
);

COMMIT;
