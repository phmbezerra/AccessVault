from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from app.core.enums import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)
    role: UserRole = UserRole.colaborador


class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
