from fastapi import HTTPException, status
from app.modules.appointments.repository import AppointmentRepository
from app.modules.appointments.schemas import AppointmentCreate, AppointmentUpdate


class AppointmentService:
    def __init__(self, repo: AppointmentRepository):
        self.repo = repo

    def list_appointments(self, limit: int = 100, offset: int = 0):
        return self.repo.list_appointments(limit, offset)

    def get_appointment(self, appointment_id: str):
        appointment = self.repo.get_appointment_by_id(appointment_id)
        if not appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return appointment

    def create_appointment(self, data: AppointmentCreate):
        return self.repo.create_appointment(data.model_dump())

    def update_appointment(self, appointment_id: str, data: AppointmentUpdate):
        update_data = data.model_dump(exclude_unset=True)
        appointment = self.repo.update_appointment(appointment_id, update_data)
        if not appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return appointment

    def delete_appointment(self, appointment_id: str):
        deleted = self.repo.delete_appointment(appointment_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return {"detail": "Appointment deleted"}
