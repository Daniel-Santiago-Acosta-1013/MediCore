-- Deploy medicore:patients to pg

BEGIN;

CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    document_id VARCHAR(50) NOT NULL UNIQUE,
    date_of_birth DATE,
    phone VARCHAR(50),
    address TEXT,
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patients_document_id ON patients(document_id);
CREATE INDEX idx_patients_user_id ON patients(user_id);

COMMIT;
