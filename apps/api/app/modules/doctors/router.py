from fastapi import APIRouter, Depends
from psycopg import Connection
from typing import List
from app.core.database import get_db
from app.core.permissions import get_current_user, require_role, UserRole
from app.modules.doctors.schemas import DoctorCreate, DoctorUpdate, DoctorOut
from app.modules.doctors.repository import DoctorRepository
from app.modules.doctors.service import DoctorService

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.get("", response_model=List[DoctorOut])
def list_doctors(
    limit: int = 100,
    offset: int = 0,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE, UserRole.RECEPTIONIST, UserRole.PATIENT)),
):
    repo = DoctorRepository(conn)
    service = DoctorService(repo)
    return service.list_doctors(limit, offset)


@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(
    doctor_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE, UserRole.RECEPTIONIST, UserRole.PATIENT)),
):
    repo = DoctorRepository(conn)
    service = DoctorService(repo)
    return service.get_doctor(doctor_id)


@router.post("", response_model=DoctorOut)
def create_doctor(
    data: DoctorCreate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = DoctorRepository(conn)
    service = DoctorService(repo)
    return service.create_doctor(data)


@router.put("/{doctor_id}", response_model=DoctorOut)
def update_doctor(
    doctor_id: str,
    data: DoctorUpdate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = DoctorRepository(conn)
    service = DoctorService(repo)
    return service.update_doctor(doctor_id, data)


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = DoctorRepository(conn)
    service = DoctorService(repo)
    return service.delete_doctor(doctor_id)
