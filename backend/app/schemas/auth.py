from pydantic import BaseModel, EmailStr, Field

from app.core.enums import UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class LoginResponse(BaseModel):
    message: str
    user_id: int
    name: str
    email: EmailStr
    role: UserRole
