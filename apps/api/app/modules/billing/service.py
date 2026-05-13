from fastapi import HTTPException, status
from app.modules.billing.repository import InvoiceRepository
from app.modules.billing.schemas import InvoiceCreate, InvoiceUpdate


class InvoiceService:
    def __init__(self, repo: InvoiceRepository):
        self.repo = repo

    def list_invoices(self, limit: int = 100, offset: int = 0):
        return self.repo.list_invoices(limit, offset)

    def get_invoice(self, invoice_id: str):
        invoice = self.repo.get_invoice_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
        return invoice

    def create_invoice(self, data: InvoiceCreate):
        return self.repo.create_invoice(data.model_dump())

    def update_invoice(self, invoice_id: str, data: InvoiceUpdate):
        update_data = data.model_dump(exclude_unset=True)
        invoice = self.repo.update_invoice(invoice_id, update_data)
        if not invoice:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
        return invoice

    def delete_invoice(self, invoice_id: str):
        deleted = self.repo.delete_invoice(invoice_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
        return {"detail": "Invoice deleted"}
