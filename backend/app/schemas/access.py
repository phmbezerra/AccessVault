from datetime import datetime
from pydantic import BaseModel

from app.core.enums import AccessLevel, AccessStatus, UserRole, SystemCriticality


class AccessCreate(BaseModel):
    user_id: int
    system_id: int
    access_level: AccessLevel
    status: AccessStatus


class AccessUpdate(BaseModel):
    access_level: AccessLevel
    status: AccessStatus
    is_active: bool


class AccessUserInfo(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True


class AccessSystemInfo(BaseModel):
    id: int
    name: str
    owner_area: str
    criticality: SystemCriticality

    class Config:
        from_attributes = True


class AccessResponse(BaseModel):
    id: int
    user_id: int
    system_id: int
    access_level: AccessLevel
    status: AccessStatus
    is_active: bool
    granted_at: datetime
    user: AccessUserInfo
    system: AccessSystemInfo

    class Config:
        from_attributes = True