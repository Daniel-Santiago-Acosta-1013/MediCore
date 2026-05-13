from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


class InvoiceCreate(BaseModel):
    patient_id: str
    appointment_id: Optional[str] = None
    amount: float
    status: Optional[str] = "PENDING"
    due_date: Optional[date] = None
    paid_at: Optional[datetime] = None


class InvoiceUpdate(BaseModel):
    patient_id: Optional[str] = None
    appointment_id: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    due_date: Optional[date] = None
    paid_at: Optional[datetime] = None


class InvoiceOut(BaseModel):
    id: str
    patient_id: str
    appointment_id: Optional[str] = None
    amount: float
    status: str
    due_date: Optional[date] = None
    paid_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
