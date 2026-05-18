from fastapi import APIRouter, Depends
from psycopg import Connection
from typing import List
from app.core.database import get_db
from app.core.permissions import get_current_user, require_role, UserRole
from app.modules.appointments.schemas import AppointmentCreate, AppointmentUpdate, AppointmentOut
from app.modules.appointments.repository import AppointmentRepository
from app.modules.appointments.service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("", response_model=List[AppointmentOut])
def list_appointments(
    limit: int = 100,
    offset: int = 0,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE, UserRole.RECEPTIONIST, UserRole.PATIENT)),
):
    repo = AppointmentRepository(conn)
    service = AppointmentService(repo)
    return service.list_appointments(limit, offset)


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(
    appointment_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE, UserRole.RECEPTIONIST, UserRole.PATIENT)),
):
    repo = AppointmentRepository(conn)
    service = AppointmentService(repo)
    return service.get_appointment(appointment_id)


@router.post("", response_model=AppointmentOut)
def create_appointment(
    data: AppointmentCreate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.RECEPTIONIST, UserRole.PATIENT)),
):
    repo = AppointmentRepository(conn)
    service = AppointmentService(repo)
    return service.create_appointment(data)


@router.put("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(
    appointment_id: str,
    data: AppointmentUpdate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.RECEPTIONIST, UserRole.DOCTOR, UserRole.PATIENT)),
):
    repo = AppointmentRepository(conn)
    service = AppointmentService(repo)
    return service.update_appointment(appointment_id, data)


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.RECEPTIONIST)),
):
    repo = AppointmentRepository(conn)
    service = AppointmentService(repo)
    return service.delete_appointment(appointment_id)
