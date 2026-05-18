from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class AppointmentCreate(BaseModel):
    patient_id: Optional[str] = None
    doctor_id: str
    appointment_date: datetime
    status: Optional[str] = "SCHEDULED"
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    patient_id: Optional[str] = None
    doctor_id: Optional[str] = None
    appointment_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentOut(BaseModel):
    id: str
    patient_id: str
    doctor_id: str
    appointment_date: datetime
    status: str
    notes: Optional[str] = None
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
