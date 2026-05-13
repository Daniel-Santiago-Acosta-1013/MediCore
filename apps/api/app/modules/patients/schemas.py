from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


class PatientCreate(BaseModel):
    user_id: Optional[str] = None
    document_id: str
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None


class PatientUpdate(BaseModel):
    user_id: Optional[str] = None
    document_id: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None


class PatientOut(BaseModel):
    id: str
    user_id: Optional[str] = None
    document_id: str
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
