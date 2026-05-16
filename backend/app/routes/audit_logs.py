from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import require_admin_or_gestor
from app.database.connection import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogResponse

router = APIRouter()


@router.get("/", response_model=list[AuditLogResponse])
def list_audit_logs(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor),
):
    logs = db.query(AuditLog).order_by(AuditLog.id.desc()).all()
    return logs