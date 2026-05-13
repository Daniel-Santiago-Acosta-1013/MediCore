from app.modules.audit.repository import AuditRepository
from app.modules.audit.schemas import AuditLogCreate


class AuditService:
    def __init__(self, repo: AuditRepository):
        self.repo = repo

    def list_logs(self, limit: int = 100, offset: int = 0):
        return self.repo.list_logs(limit, offset)

    def get_log(self, log_id: str):
        return self.repo.get_log_by_id(log_id)

    def create_log(self, data: AuditLogCreate):
        return self.repo.create_log(data.model_dump())
