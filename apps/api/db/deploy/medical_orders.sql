-- Deploy medicore:medical_orders to pg

BEGIN;

CREATE TABLE medical_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    medical_record_id UUID NOT NULL REFERENCES medical_records(id) ON DELETE CASCADE,
    doctor_id UUID REFERENCES doctors(id) ON DELETE SET NULL,
    order_type VARCHAR(100) NOT NULL CHECK (order_type IN ('LAB', 'IMAGE', 'PRESCRIPTION', 'PROCEDURE', 'OTHER')),
    description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_medical_orders_medical_record_id ON medical_orders(medical_record_id);
CREATE INDEX idx_medical_orders_doctor_id ON medical_orders(doctor_id);
CREATE INDEX idx_medical_orders_status ON medical_orders(status);

COMMIT;
