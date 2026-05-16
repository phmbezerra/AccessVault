from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.audit import create_audit_log
from app.core.deps import require_admin_or_gestor
from app.database.connection import get_db
from app.models.system import System
from app.models.user import User
from app.schemas.system import SystemCreate, SystemResponse, SystemUpdate

router = APIRouter()


@router.get("/", response_model=list[SystemResponse])
def list_systems(db: Session = Depends(get_db)):
    systems = db.query(System).order_by(System.id.desc()).all()
    return systems


@router.get("/{system_id}", response_model=SystemResponse)
def get_system(system_id: int, db: Session = Depends(get_db)):
    system = db.query(System).filter(System.id == system_id).first()

    if not system:
        raise HTTPException(status_code=404, detail="Sistema não encontrado.")

    return system


@router.post("/", response_model=SystemResponse)
def create_system(
    system: SystemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_gestor),
):
    existing_system = db.query(System).filter(System.name == system.name).first()

    if existing_system:
        raise HTTPException(status_code=400, detail="Sistema já cadastrado.")

    new_system = System(
        name=system.name,
        description=system.description,
        owner_area=system.owner_area,
        criticality=system.criticality,
        is_active=True,
    )

    db.add(new_system)
    db.commit()
    db.refresh(new_system)

    create_audit_log(
        db=db,
        action="create_system",
        entity_type="system",
        entity_id=new_system.id,
        entity_name=new_system.name,
        details=f"Sistema criado para a área {new_system.owner_area}.",
        actor=current_user,
    )

    return new_system


@router.put("/{system_id}", response_model=SystemResponse)
def update_system(
    system_id: int,
    system_data: SystemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_gestor),
):
    system = db.query(System).filter(System.id == system_id).first()

    if not system:
        raise HTTPException(status_code=404, detail="Sistema não encontrado.")

    existing_system = (
        db.query(System)
        .filter(System.name == system_data.name, System.id != system_id)
        .first()
    )
    if existing_system:
        raise HTTPException(status_code=400, detail="Sistema já cadastrado.")

    system.name = system_data.name
    system.description = system_data.description
    system.owner_area = system_data.owner_area
    system.criticality = system_data.criticality
    system.is_active = system_data.is_active

    db.commit()
    db.refresh(system)

    create_audit_log(
        db=db,
        action="update_system",
        entity_type="system",
        entity_id=system.id,
        entity_name=system.name,
        details=f"Sistema atualizado para a área {system.owner_area}.",
        actor=current_user,
    )

    return system


@router.delete("/{system_id}", response_model=SystemResponse)
def deactivate_system(
    system_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_gestor),
):
    system = db.query(System).filter(System.id == system_id).first()

    if not system:
        raise HTTPException(status_code=404, detail="Sistema não encontrado.")

    system.is_active = False

    db.commit()
    db.refresh(system)

    create_audit_log(
        db=db,
        action="deactivate_system",
        entity_type="system",
        entity_id=system.id,
        entity_name=system.name,
        details="Sistema desativado.",
        actor=current_user,
    )

    return system