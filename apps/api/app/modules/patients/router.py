from fastapi import APIRouter, Depends
from psycopg import Connection
from typing import List
from app.core.database import get_db
from app.core.permissions import get_current_user, require_role, UserRole
from app.modules.patients.schemas import PatientCreate, PatientUpdate, PatientOut
from app.modules.patients.repository import PatientRepository
from app.modules.patients.service import PatientService

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("", response_model=List[PatientOut])
def list_patients(
    limit: int = 100,
    offset: int = 0,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE, UserRole.RECEPTIONIST)),
):
    repo = PatientRepository(conn)
    service = PatientService(repo)
    return service.list_patients(limit, offset)


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(
    patient_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE, UserRole.RECEPTIONIST)),
):
    repo = PatientRepository(conn)
    service = PatientService(repo)
    return service.get_patient(patient_id)


@router.post("", response_model=PatientOut)
def create_patient(
    data: PatientCreate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.RECEPTIONIST)),
):
    repo = PatientRepository(conn)
    service = PatientService(repo)
    return service.create_patient(data)


@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: str,
    data: PatientUpdate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.RECEPTIONIST)),
):
    repo = PatientRepository(conn)
    service = PatientService(repo)
    return service.update_patient(patient_id, data)


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = PatientRepository(conn)
    service = PatientService(repo)
    return service.delete_patient(patient_id)
