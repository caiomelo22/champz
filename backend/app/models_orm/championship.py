from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

from app.db.base import Base


class Championship(Base):
    __tablename__ = "championship"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    owner_id = Column(CHAR(36), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum("draft", "games", "complete", name="championship_status"), default="draft", nullable=False)
    budget_default = Column(Integer, default=250, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    owner = relationship("User", back_populates="championships", lazy="selectin")
    participants = relationship("Participant", back_populates="championship", cascade="all, delete-orphan", lazy="selectin")
    groups = relationship("Group", back_populates="championship", cascade="all, delete-orphan", lazy="selectin")
