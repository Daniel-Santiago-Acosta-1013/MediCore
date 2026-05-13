from fastapi import HTTPException, status
from app.modules.patients.repository import PatientRepository
from app.modules.patients.schemas import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self, repo: PatientRepository):
        self.repo = repo

    def list_patients(self, limit: int = 100, offset: int = 0):
        return self.repo.list_patients(limit, offset)

    def get_patient(self, patient_id: str):
        patient = self.repo.get_patient_by_id(patient_id)
        if not patient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return patient

    def create_patient(self, data: PatientCreate):
        return self.repo.create_patient(data.model_dump())

    def update_patient(self, patient_id: str, data: PatientUpdate):
        update_data = data.model_dump(exclude_unset=True)
        patient = self.repo.update_patient(patient_id, update_data)
        if not patient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return patient

    def delete_patient(self, patient_id: str):
        deleted = self.repo.delete_patient(patient_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return {"detail": "Patient deleted"}
