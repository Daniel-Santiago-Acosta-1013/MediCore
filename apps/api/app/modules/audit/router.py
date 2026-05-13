from fastapi import APIRouter, Depends
from psycopg import Connection
from typing import List
from app.core.database import get_db
from app.core.permissions import get_current_user, require_role, UserRole
from app.modules.audit.schemas import AuditLogCreate, AuditLogOut
from app.modules.audit.repository import AuditRepository
from app.modules.audit.service import AuditService

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])


@router.get("", response_model=List[AuditLogOut])
def list_logs(
    limit: int = 100,
    offset: int = 0,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = AuditRepository(conn)
    service = AuditService(repo)
    return service.list_logs(limit, offset)


@router.get("/{log_id}", response_model=AuditLogOut)
def get_log(
    log_id: str,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = AuditRepository(conn)
    service = AuditService(repo)
    return service.get_log(log_id)


@router.post("", response_model=AuditLogOut)
def create_log(
    data: AuditLogCreate,
    conn: Connection = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    repo = AuditRepository(conn)
    service = AuditService(repo)
    return service.create_log(data)
