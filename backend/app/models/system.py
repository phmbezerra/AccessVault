from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database.base import Base


class System(Base):
    __tablename__ = "systems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    owner_area = Column(String, nullable=False)
    criticality = Column(String, nullable=False, default="media")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
