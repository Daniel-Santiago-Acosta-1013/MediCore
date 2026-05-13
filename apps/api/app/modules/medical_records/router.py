from fastapi import APIRouter, Depends
from psycopg import Connection
from typing import List
from app.core.database import get_db
from app.core.permissions import get_current_user, require_role, UserRole
from app.modules.medical_records.schemas import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordOut
from app.modules.medical_records.repository import MedicalRecordRepository
from app.modules.medical_records.service import MedicalRecordService

router = APIRouter(prefix="/medical-records", tags=["medical-records"])


@router.get("", response_model=List[MedicalRecordOut])
def list_records(
    limit: int = 100,
    offset: int = 0,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE)),
):
    repo = MedicalRecordRepository(conn)
    service = MedicalRecordService(repo)
    return service.list_records(limit, offset)


@router.get("/{record_id}", response_model=MedicalRecordOut)
def get_record(
    record_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE)),
):
    repo = MedicalRecordRepository(conn)
    service = MedicalRecordService(repo)
    return service.get_record(record_id)


@router.post("", response_model=MedicalRecordOut)
def create_record(
    data: MedicalRecordCreate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR)),
):
    repo = MedicalRecordRepository(conn)
    service = MedicalRecordService(repo)
    return service.create_record(data)


@router.put("/{record_id}", response_model=MedicalRecordOut)
def update_record(
    record_id: str,
    data: MedicalRecordUpdate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR)),
):
    repo = MedicalRecordRepository(conn)
    service = MedicalRecordService(repo)
    return service.update_record(record_id, data)


@router.delete("/{record_id}")
def delete_record(
    record_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = MedicalRecordRepository(conn)
    service = MedicalRecordService(repo)
    return service.delete_record(record_id)
