from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.system import System
from app.schemas.system import SystemCreate, SystemResponse, SystemUpdate

router = APIRouter()


@router.get("/", response_model=list[SystemResponse])
def list_systems(
    is_active: bool | None = None,
    criticality: str | None = None,
    owner_area: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(System)

    if is_active is not None:
        query = query.filter(System.is_active == is_active)

    if criticality is not None:
        query = query.filter(System.criticality == criticality)

    if owner_area is not None:
        query = query.filter(System.owner_area == owner_area)

    return query.all()


@router.get("/{system_id}", response_model=SystemResponse)
def get_system(system_id: int, db: Session = Depends(get_db)):
    system = db.query(System).filter(System.id == system_id).first()

    if not system:
        raise HTTPException(status_code=404, detail="Sistema não encontrado.")

    return system


@router.post("/", response_model=SystemResponse)
def create_system(data: SystemCreate, db: Session = Depends(get_db)):
    existing_system = db.query(System).filter(System.name == data.name).first()

    if existing_system:
        raise HTTPException(status_code=400, detail="Já existe um sistema com esse nome.")

    new_system = System(
        name=data.name,
        description=data.description,
        owner_area=data.owner_area,
        criticality=data.criticality,
    )

    db.add(new_system)
    db.commit()
    db.refresh(new_system)

    return new_system


@router.put("/{system_id}", response_model=SystemResponse)
def update_system(system_id: int, data: SystemUpdate, db: Session = Depends(get_db)):
    system = db.query(System).filter(System.id == system_id).first()

    if not system:
        raise HTTPException(status_code=404, detail="Sistema não encontrado.")

    existing_name = db.query(System).filter(System.name == data.name, System.id != system_id).first()
    if existing_name:
        raise HTTPException(status_code=400, detail="Já existe outro sistema com esse nome.")

    system.name = data.name
    system.description = data.description
    system.owner_area = data.owner_area
    system.criticality = data.criticality
    system.is_active = data.is_active

    db.commit()
    db.refresh(system)

    return system
