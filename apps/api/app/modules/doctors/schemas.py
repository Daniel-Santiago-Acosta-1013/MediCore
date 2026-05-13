from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class DoctorCreate(BaseModel):
    user_id: str
    license_number: str
    specialty: str
    phone: Optional[str] = None


class DoctorUpdate(BaseModel):
    user_id: Optional[str] = None
    license_number: Optional[str] = None
    specialty: Optional[str] = None
    phone: Optional[str] = None


class DoctorOut(BaseModel):
    id: str
    user_id: str
    license_number: str
    specialty: str
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
