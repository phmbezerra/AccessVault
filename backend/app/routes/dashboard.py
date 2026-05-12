from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.models.system import System
from app.models.access import Access
from app.schemas.dashboard import DashboardSummaryResponse

router = APIRouter()


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    inactive_users = db.query(User).filter(User.is_active == False).count()

    total_systems = db.query(System).count()
    active_systems = db.query(System).filter(System.is_active == True).count()
    inactive_systems = db.query(System).filter(System.is_active == False).count()

    total_accesses = db.query(Access).count()
    active_accesses = db.query(Access).filter(Access.is_active == True).count()
    revoked_accesses = db.query(Access).filter(Access.status == "revogado").count()
    pending_accesses = db.query(Access).filter(Access.status == "pendente").count()

    return DashboardSummaryResponse(
        total_users=total_users,
        active_users=active_users,
        inactive_users=inactive_users,
        total_systems=total_systems,
        active_systems=active_systems,
        inactive_systems=inactive_systems,
        total_accesses=total_accesses,
        active_accesses=active_accesses,
        revoked_accesses=revoked_accesses,
        pending_accesses=pending_accesses,
    )
