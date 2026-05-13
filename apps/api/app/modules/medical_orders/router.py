from fastapi import APIRouter, Depends
from psycopg import Connection
from typing import List
from app.core.database import get_db
from app.core.permissions import get_current_user, require_role, UserRole
from app.modules.medical_orders.schemas import MedicalOrderCreate, MedicalOrderUpdate, MedicalOrderOut
from app.modules.medical_orders.repository import MedicalOrderRepository
from app.modules.medical_orders.service import MedicalOrderService

router = APIRouter(prefix="/medical-orders", tags=["medical-orders"])


@router.get("", response_model=List[MedicalOrderOut])
def list_orders(
    limit: int = 100,
    offset: int = 0,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE)),
):
    repo = MedicalOrderRepository(conn)
    service = MedicalOrderService(repo)
    return service.list_orders(limit, offset)


@router.get("/{order_id}", response_model=MedicalOrderOut)
def get_order(
    order_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE)),
):
    repo = MedicalOrderRepository(conn)
    service = MedicalOrderService(repo)
    return service.get_order(order_id)


@router.post("", response_model=MedicalOrderOut)
def create_order(
    data: MedicalOrderCreate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR)),
):
    repo = MedicalOrderRepository(conn)
    service = MedicalOrderService(repo)
    return service.create_order(data)


@router.put("/{order_id}", response_model=MedicalOrderOut)
def update_order(
    order_id: str,
    data: MedicalOrderUpdate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR, UserRole.NURSE)),
):
    repo = MedicalOrderRepository(conn)
    service = MedicalOrderService(repo)
    return service.update_order(order_id, data)


@router.delete("/{order_id}")
def delete_order(
    order_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = MedicalOrderRepository(conn)
    service = MedicalOrderService(repo)
    return service.delete_order(order_id)
