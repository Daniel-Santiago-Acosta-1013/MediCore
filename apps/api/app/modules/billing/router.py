from fastapi import APIRouter, Depends
from psycopg import Connection
from typing import List
from app.core.database import get_db
from app.core.permissions import get_current_user, require_role, UserRole
from app.modules.billing.schemas import InvoiceCreate, InvoiceUpdate, InvoiceOut
from app.modules.billing.repository import InvoiceRepository
from app.modules.billing.service import InvoiceService

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("", response_model=List[InvoiceOut])
def list_invoices(
    limit: int = 100,
    offset: int = 0,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.BILLING)),
):
    repo = InvoiceRepository(conn)
    service = InvoiceService(repo)
    return service.list_invoices(limit, offset)


@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(
    invoice_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.BILLING)),
):
    repo = InvoiceRepository(conn)
    service = InvoiceService(repo)
    return service.get_invoice(invoice_id)


@router.post("", response_model=InvoiceOut)
def create_invoice(
    data: InvoiceCreate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.BILLING)),
):
    repo = InvoiceRepository(conn)
    service = InvoiceService(repo)
    return service.create_invoice(data)


@router.put("/{invoice_id}", response_model=InvoiceOut)
def update_invoice(
    invoice_id: str,
    data: InvoiceUpdate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN, UserRole.BILLING)),
):
    repo = InvoiceRepository(conn)
    service = InvoiceService(repo)
    return service.update_invoice(invoice_id, data)


@router.delete("/{invoice_id}")
def delete_invoice(
    invoice_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = InvoiceRepository(conn)
    service = InvoiceService(repo)
    return service.delete_invoice(invoice_id)
