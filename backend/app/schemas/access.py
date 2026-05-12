from datetime import datetime
from pydantic import BaseModel, Field


class AccessCreate(BaseModel):
    user_id: int
    system_id: int
    access_level: str = Field(..., min_length=2, max_length=50)
    status: str = Field(..., min_length=2, max_length=30)


class AccessUpdate(BaseModel):
    access_level: str = Field(..., min_length=2, max_length=50)
    status: str = Field(..., min_length=2, max_length=30)
    is_active: bool


class AccessResponse(BaseModel):
    id: int
    user_id: int
    system_id: int
    access_level: str
    status: str
    is_active: bool
    granted_at: datetime

    class Config:
        from_attributes = True
