from fastapi import APIRouter, Depends, HTTPException, status
from psycopg import Connection
from typing import List, Optional
from app.core.database import get_db
from app.core.permissions import get_current_user, require_role, UserRole
from app.modules.appointments.schemas import AppointmentCreate, AppointmentUpdate, AppointmentOut
from app.modules.appointments.repository import AppointmentRepository
from app.modules.appointments.service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["appointments"])


def _resolve_patient_id(conn: Connection, user_id: str) -> Optional[str]:
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM patients WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        return row[0] if row else None


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
    # Resolve patient_id from current_user if not provided (patient booking for themselves)
    # or if provided, resolve from patients table (patient_id is a user_id in the request)
    target_user_id = data.patient_id or str(current_user["id"])
    real_patient_id = _resolve_patient_id(conn, target_user_id)
    if not real_patient_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient profile not found for the given user",
        )
    data.patient_id = real_patient_id

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
    if data.patient_id is not None:
        real_patient_id = _resolve_patient_id(conn, data.patient_id)
        if not real_patient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Patient profile not found for the given user",
            )
        data.patient_id = real_patient_id

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
