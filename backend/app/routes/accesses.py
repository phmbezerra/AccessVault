from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.access import Access
from app.models.system import System
from app.models.user import User
from app.schemas.access import AccessCreate, AccessResponse, AccessUpdate
from app.core.deps import require_admin_or_gestor

router = APIRouter()


@router.get("/", response_model=list[AccessResponse])
def list_accesses(
    is_active: bool | None = None,
    status: str | None = None,
    access_level: str | None = None,
    user_id: int | None = None,
    system_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Access)

    if is_active is not None:
        query = query.filter(Access.is_active == is_active)

    if status is not None:
        query = query.filter(Access.status == status)

    if access_level is not None:
        query = query.filter(Access.access_level == access_level)

    if user_id is not None:
        query = query.filter(Access.user_id == user_id)

    if system_id is not None:
        query = query.filter(Access.system_id == system_id)

    return query.all()


@router.get("/{access_id}", response_model=AccessResponse)
def get_access(access_id: int, db: Session = Depends(get_db)):
    access = db.query(Access).filter(Access.id == access_id).first()

    if not access:
        raise HTTPException(status_code=404, detail="Acesso não encontrado.")

    return access


@router.post("/", response_model=AccessResponse)
def create_access(
    access: AccessCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor),
):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    system = db.query(System).filter(System.id == data.system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="Sistema não encontrado.")

    existing_access = db.query(Access).filter(
        Access.user_id == data.user_id,
        Access.system_id == data.system_id,
        Access.is_active == True
    ).first()

    if existing_access:
        raise HTTPException(status_code=400, detail="Esse usuário já possui acesso ativo a esse sistema.")

    new_access = Access(
        user_id=data.user_id,
        system_id=data.system_id,
        access_level=data.access_level,
        status=data.status,
    )

    db.add(new_access)
    db.commit()
    db.refresh(new_access)

    return new_access


@router.put("/{access_id}", response_model=AccessResponse)
def update_access(access_id: int, data: AccessUpdate, db: Session = Depends(get_db)):
    access = db.query(Access).filter(Access.id == access_id).first()

    if not access:
        raise HTTPException(status_code=404, detail="Acesso não encontrado.")

    access.access_level = data.access_level
    access.status = data.status
    access.is_active = data.is_active

    db.commit()
    db.refresh(access)

    return access


@router.delete("/{access_id}", response_model=AccessResponse)
def deactivate_access(access_id: int, db: Session = Depends(get_db)):
    access = db.query(Access).filter(Access.id == access_id).first()

    if not access:
        raise HTTPException(status_code=404, detail="Acesso não encontrado.")

    access.is_active = False
    access.status = "revogado"

    db.commit()
    db.refresh(access)

    return access
