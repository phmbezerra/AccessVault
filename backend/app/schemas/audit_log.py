from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    actor_user_id: Optional[int]
    actor_email: Optional[str]
    action: str
    entity_type: str
    entity_id: Optional[int]
    entity_name: Optional[str]
    details: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True