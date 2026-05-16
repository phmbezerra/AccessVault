from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.audit import create_audit_log
from app.core.deps import get_current_user_optional, require_admin_or_gestor
from app.core.security import hash_password
from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.desc()).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    return user


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    total_users = db.query(User).count()

    if total_users > 0:
        if current_user is None:
            raise HTTPException(status_code=401, detail="Não autenticado.")

        if current_user.role not in ["admin", "gestor"]:
            raise HTTPException(
                status_code=403,
                detail="Você não tem permissão para executar esta ação.",
            )

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    create_audit_log(
        db=db,
        action="create_user",
        entity_type="user",
        entity_id=new_user.id,
        entity_name=new_user.name,
        details=f"Usuário criado com perfil {new_user.role}.",
        actor=current_user,
    )

    return new_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_gestor),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    existing_email = (
        db.query(User)
        .filter(User.email == user_data.email, User.id != user_id)
        .first()
    )
    if existing_email:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    create_audit_log(
        db=db,
        action="update_user",
        entity_type="user",
        entity_id=user.id,
        entity_name=user.name,
        details=f"Usuário atualizado para perfil {user.role}.",
        actor=current_user,
    )

    return user


@router.delete("/{user_id}", response_model=UserResponse)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_gestor),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    user.is_active = False

    db.commit()
    db.refresh(user)

    create_audit_log(
        db=db,
        action="deactivate_user",
        entity_type="user",
        entity_id=user.id,
        entity_name=user.name,
        details="Usuário desativado.",
        actor=current_user,
    )

    return user