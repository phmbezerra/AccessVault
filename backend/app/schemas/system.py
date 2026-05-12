from datetime import datetime
from pydantic import BaseModel, Field

from app.core.enums import SystemCriticality


class SystemCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    owner_area: str = Field(..., min_length=2, max_length=100)
    criticality: SystemCriticality


class SystemUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    owner_area: str = Field(..., min_length=2, max_length=100)
    criticality: SystemCriticality
    is_active: bool


class SystemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_area: str
    criticality: SystemCriticality
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
