-- Deploy medicore:seed_profiles to pg

BEGIN;

-- Insertar perfiles de doctor para los 10 usuarios con rol DOCTOR
WITH doctor_users AS (
    SELECT id, row_number() OVER () as rn
    FROM users
    WHERE role = 'DOCTOR'
      AND email LIKE '%@medicore.com'
)
INSERT INTO doctors (user_id, license_number, specialty, phone)
SELECT
    id,
    'MED-' || LPAD(rn::text, 5, '0'),
    (ARRAY[
        'Cardiología',
        'Pediatría',
        'Neurología',
        'Dermatología',
        'Ortopedia',
        'Ginecología',
        'Oftalmología',
        'Psiquiatría',
        'Urología',
        'Endocrinología'
    ])[rn],
    '555-01' || LPAD(rn::text, 2, '0')
FROM doctor_users;

-- Insertar perfiles de paciente para los 10 usuarios con rol PATIENT
WITH patient_users AS (
    SELECT id, row_number() OVER () as rn
    FROM users
    WHERE role = 'PATIENT'
      AND email LIKE '%@medicore.com'
)
INSERT INTO patients (
    user_id,
    document_id,
    date_of_birth,
    phone,
    address,
    emergency_contact_name,
    emergency_contact_phone
)
SELECT
    id,
    'DOC-' || LPAD(rn::text, 8, '0'),
    CURRENT_DATE - INTERVAL '22 years' - (rn * INTERVAL '1 year'),
    '555-10' || LPAD(rn::text, 2, '0'),
    'Calle ' || rn || ' #' || (rn * 10) || '-10, Ciudad Médica',
    'Contacto Emergencia ' || rn,
    '555-20' || LPAD(rn::text, 2, '0')
FROM patient_users;

COMMIT;
