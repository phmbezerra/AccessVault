from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos.")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos.")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuário inativo.")

    token = create_access_token(
        {
            "sub": user.email,
            "user_id": user.id,
            "role": user.role,
            "name": user.name,
        }
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
    )