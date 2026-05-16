from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_admin_or_gestor
from app.database.connection import get_db
from app.models.access import Access
from app.models.request import AccessRequest
from app.models.system import System
from app.models.user import User
from app.schemas.request import (
    AccessRequestCreate,
    AccessRequestResponse,
    AccessRequestReview,
)

router = APIRouter()


@router.get("/", response_model=list[AccessRequestResponse])
def list_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    requests = db.query(AccessRequest).order_by(AccessRequest.id.desc()).all()
    return requests


@router.post("/", response_model=AccessRequestResponse)
def create_request(
    data: AccessRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    target_user = db.query(User).filter(User.id == data.target_user_id).first()
    system = db.query(System).filter(System.id == data.system_id).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="Usuário de destino não encontrado.")

    if not system:
        raise HTTPException(status_code=404, detail="Sistema não encontrado.")

    request = AccessRequest(
        requester_id=current_user.id,
        target_user_id=data.target_user_id,
        system_id=data.system_id,
        access_level=data.access_level,
        justification=data.justification,
        status="pendente",
    )

    db.add(request)
    db.commit()
    db.refresh(request)
    return request


@router.put("/{request_id}/review", response_model=AccessRequestResponse)
def review_request(
    request_id: int,
    data: AccessRequestReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_gestor),
):
    request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()

    if not request:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

    if request.status != "pendente":
        raise HTTPException(status_code=400, detail="Essa solicitação já foi analisada.")

    if data.status not in ["aprovado", "rejeitado"]:
        raise HTTPException(status_code=400, detail="Status inválido para revisão.")

    request.status = data.status
    request.reviewer_note = data.reviewer_note
    request.reviewed_at = datetime.now(timezone.utc)

    if data.status == "aprovado":
        existing_access = (
            db.query(Access)
            .filter(
                Access.user_id == request.target_user_id,
                Access.system_id == request.system_id,
                Access.access_level == request.access_level,
                Access.is_active == True,
            )
            .first()
        )

        if not existing_access:
            new_access = Access(
                user_id=request.target_user_id,
                system_id=request.system_id,
                access_level=request.access_level,
                status="ativo",
                is_active=True,
            )
            db.add(new_access)

    db.commit()
    db.refresh(request)
    return request