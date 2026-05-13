from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class MedicalRecordCreate(BaseModel):
    patient_id: str
    doctor_id: Optional[str] = None
    appointment_id: Optional[str] = None
    diagnosis: str
    treatment: Optional[str] = None
    notes: Optional[str] = None


class MedicalRecordUpdate(BaseModel):
    patient_id: Optional[str] = None
    doctor_id: Optional[str] = None
    appointment_id: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None


class MedicalRecordOut(BaseModel):
    id: str
    patient_id: str
    doctor_id: Optional[str] = None
    appointment_id: Optional[str] = None
    diagnosis: str
    treatment: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
