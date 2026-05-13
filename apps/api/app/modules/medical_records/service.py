from fastapi import HTTPException, status
from app.modules.medical_records.repository import MedicalRecordRepository
from app.modules.medical_records.schemas import MedicalRecordCreate, MedicalRecordUpdate


class MedicalRecordService:
    def __init__(self, repo: MedicalRecordRepository):
        self.repo = repo

    def list_records(self, limit: int = 100, offset: int = 0):
        return self.repo.list_records(limit, offset)

    def get_record(self, record_id: str):
        record = self.repo.get_record_by_id(record_id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical record not found")
        return record

    def create_record(self, data: MedicalRecordCreate):
        return self.repo.create_record(data.model_dump())

    def update_record(self, record_id: str, data: MedicalRecordUpdate):
        update_data = data.model_dump(exclude_unset=True)
        record = self.repo.update_record(record_id, update_data)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical record not found")
        return record

    def delete_record(self, record_id: str):
        deleted = self.repo.delete_record(record_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical record not found")
        return {"detail": "Medical record deleted"}
