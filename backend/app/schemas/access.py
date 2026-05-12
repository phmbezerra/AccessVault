from datetime import datetime
from pydantic import BaseModel

from app.core.enums import AccessLevel, AccessStatus


class AccessCreate(BaseModel):
    user_id: int
    system_id: int
    access_level: AccessLevel
    status: AccessStatus


class AccessUpdate(BaseModel):
    access_level: AccessLevel
    status: AccessStatus
    is_active: bool


class AccessResponse(BaseModel):
    id: int
    user_id: int
    system_id: int
    access_level: AccessLevel
    status: AccessStatus
    is_active: bool
    granted_at: datetime

    class Config:
        from_attributes = True
