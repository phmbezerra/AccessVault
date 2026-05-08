from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos.")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos.")

    return LoginResponse(
        message="Login realizado com sucesso.",
        user_id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
    )
