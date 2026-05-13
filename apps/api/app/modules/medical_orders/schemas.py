from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class MedicalOrderCreate(BaseModel):
    medical_record_id: str
    doctor_id: Optional[str] = None
    order_type: str
    description: str
    status: Optional[str] = "PENDING"


class MedicalOrderUpdate(BaseModel):
    medical_record_id: Optional[str] = None
    doctor_id: Optional[str] = None
    order_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class MedicalOrderOut(BaseModel):
    id: str
    medical_record_id: str
    doctor_id: Optional[str] = None
    order_type: str
    description: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
