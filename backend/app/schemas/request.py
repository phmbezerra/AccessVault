from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AccessRequestCreate(BaseModel):
    target_user_id: int
    system_id: int
    access_level: str
    justification: str


class AccessRequestReview(BaseModel):
    status: str
    reviewer_note: Optional[str] = None


class AccessRequestResponse(BaseModel):
    id: int
    requester_id: int
    target_user_id: int
    system_id: int
    access_level: str
    justification: str
    status: str
    reviewer_note: Optional[str]
    is_active: bool
    created_at: Optional[datetime]
    reviewed_at: Optional[datetime]

    class Config:
        from_attributes = True