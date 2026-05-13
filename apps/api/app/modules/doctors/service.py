from fastapi import HTTPException, status
from app.modules.doctors.repository import DoctorRepository
from app.modules.doctors.schemas import DoctorCreate, DoctorUpdate


class DoctorService:
    def __init__(self, repo: DoctorRepository):
        self.repo = repo

    def list_doctors(self, limit: int = 100, offset: int = 0):
        return self.repo.list_doctors(limit, offset)

    def get_doctor(self, doctor_id: str):
        doctor = self.repo.get_doctor_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return doctor

    def create_doctor(self, data: DoctorCreate):
        return self.repo.create_doctor(data.model_dump())

    def update_doctor(self, doctor_id: str, data: DoctorUpdate):
        update_data = data.model_dump(exclude_unset=True)
        doctor = self.repo.update_doctor(doctor_id, update_data)
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return doctor

    def delete_doctor(self, doctor_id: str):
        deleted = self.repo.delete_doctor(doctor_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return {"detail": "Doctor deleted"}
