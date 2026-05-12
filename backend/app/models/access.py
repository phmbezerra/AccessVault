from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Access(Base):
    __tablename__ = "accesses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    system_id = Column(Integer, ForeignKey("systems.id"), nullable=False)
    access_level = Column(String, nullable=False)
    status = Column(String, nullable=False, default="ativo")
    is_active = Column(Boolean, default=True)
    granted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    system = relationship("System")
