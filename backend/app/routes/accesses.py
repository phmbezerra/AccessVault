from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.core.audit import create_audit_log
from app.core.deps import require_admin_or_gestor
from app.database.connection import get_db
from app.models.access import Access
from app.models.system import System
from app.models.user import User
from app.schemas.access import AccessCreate, AccessResponse, AccessUpdate

router = APIRouter()


@router.get("/", response_model=list[AccessResponse])
def list_accesses(db: Session = Depends(get_db)):
    accesses = (
        db.query(Access)
        .options(joinedload(Access.user), joinedload(Access.system))
        .order_by(Access.id.desc())
        .all()
    )
    return accesses


@router.get("/{access_id}", response_model=AccessResponse)
def get_access(access_id: int, db: Session = Depends(get_db)):
    access = (
        db.query(Access)
        .options(joinedload(Access.user), joinedload(Access.system))
        .filter(Access.id == access_id)
        .first()
    )

    if not access:
        raise HTTPException(status_code=404, detail="Acesso não encontrado.")

    return access


@router.post("/", response_model=AccessResponse)
def create_access(
    access: AccessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_gestor),
):
    user = db.query(User).filter(User.id == access.user_id).first()
    system = db.query(System).filter(System.id == access.system_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if not system:
        raise HTTPException(status_code=404, detail="Sistema não encontrado.")

    new_access = Access(
        user_id=access.user_id,
        system_id=access.system_id,
        access_level=access.access_level,
        status=access.status,
        is_active=True,
    )

    db.add(new_access)
    db.commit()
    db.refresh(new_access)

    create_audit_log(
        db=db,
        action="create_access",
        entity_type="access",
        entity_id=new_access.id,
        entity_name=f"user:{new_access.user_id}-system:{new_access.system_id}",
        details=f"Acesso {new_access.access_level} criado com status {new_access.status}.",
        actor=current_user,
    )

    access_with_relations = (
        db.query(Access)
        .options(joinedload(Access.user), joinedload(Access.system))
        .filter(Access.id == new_access.id)
        .first()
    )

    return access_with_relations


@router.put("/{access_id}", response_model=AccessResponse)
def update_access(
    access_id: int,
    access_data: AccessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_gestor),
):
    access = db.query(Access).filter(Access.id == access_id).first()

    if not access:
        raise HTTPException(status_code=404, detail="Acesso não encontrado.")

    access.access_level = access_data.access_level
    access.status = access_data.status
    access.is_active = access_data.is_active

    db.commit()
    db.refresh(access)

    create_audit_log(
        db=db,
        action="update_access",
        entity_type="access",
        entity_id=access.id,
        entity_name=f"user:{access.user_id}-system:{access.system_id}",
        details=f"Acesso atualizado para nível {access.access_level} e status {access.status}.",
        actor=current_user,
    )

    access_with_relations = (
        db.query(Access)
        .options(joinedload(Access.user), joinedload(Access.system))
        .filter(Access.id == access.id)
        .first()
    )

    return access_with_relations


@router.delete("/{access_id}", response_model=AccessResponse)
def deactivate_access(
    access_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_gestor),
):
    access = db.query(Access).filter(Access.id == access_id).first()

    if not access:
        raise HTTPException(status_code=404, detail="Acesso não encontrado.")

    access.is_active = False
    access.status = "revogado"

    db.commit()
    db.refresh(access)

    create_audit_log(
        db=db,
        action="deactivate_access",
        entity_type="access",
        entity_id=access.id,
        entity_name=f"user:{access.user_id}-system:{access.system_id}",
        details="Acesso revogado/desativado.",
        actor=current_user,
    )

    access_with_relations = (
        db.query(Access)
        .options(joinedload(Access.user), joinedload(Access.system))
        .filter(Access.id == access.id)
        .first()
    )

    return access_with_relations