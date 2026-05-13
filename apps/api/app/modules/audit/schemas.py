from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any


class AuditLogCreate(BaseModel):
    table_name: str
    record_id: str
    action: str
    old_data: Optional[Dict[str, Any]] = None
    new_data: Optional[Dict[str, Any]] = None
    performed_by: Optional[str] = None


class AuditLogOut(BaseModel):
    id: str
    table_name: str
    record_id: str
    action: str
    old_data: Optional[Dict[str, Any]] = None
    new_data: Optional[Dict[str, Any]] = None
    performed_by: Optional[str] = None
    created_at: Optional[datetime] = None
