from datetime import datetime
from pydantic import BaseModel, Field


class SystemCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    owner_area: str = Field(..., min_length=2, max_length=100)
    criticality: str = Field(..., min_length=3, max_length=20)


class SystemUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    owner_area: str = Field(..., min_length=2, max_length=100)
    criticality: str = Field(..., min_length=3, max_length=20)
    is_active: bool


class SystemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_area: str
    criticality: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
