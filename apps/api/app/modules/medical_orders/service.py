from fastapi import HTTPException, status
from app.modules.medical_orders.repository import MedicalOrderRepository
from app.modules.medical_orders.schemas import MedicalOrderCreate, MedicalOrderUpdate


class MedicalOrderService:
    def __init__(self, repo: MedicalOrderRepository):
        self.repo = repo

    def list_orders(self, limit: int = 100, offset: int = 0):
        return self.repo.list_orders(limit, offset)

    def get_order(self, order_id: str):
        order = self.repo.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical order not found")
        return order

    def create_order(self, data: MedicalOrderCreate):
        return self.repo.create_order(data.model_dump())

    def update_order(self, order_id: str, data: MedicalOrderUpdate):
        update_data = data.model_dump(exclude_unset=True)
        order = self.repo.update_order(order_id, update_data)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical order not found")
        return order

    def delete_order(self, order_id: str):
        deleted = self.repo.delete_order(order_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical order not found")
        return {"detail": "Medical order deleted"}
