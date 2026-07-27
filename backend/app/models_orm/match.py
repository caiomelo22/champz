from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Match(Base):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("group.id", ondelete="CASCADE"), nullable=False)
    participant_1_id = Column(Integer, ForeignKey("participant.id", ondelete="CASCADE"), nullable=False)
    participant_2_id = Column(Integer, ForeignKey("participant.id", ondelete="CASCADE"), nullable=False)
    goals_1 = Column(Integer, nullable=True)
    goals_2 = Column(Integer, nullable=True)
    round = Column(Integer, nullable=True)
    penalties = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    group = relationship("Group", back_populates="matches")
    participant_1 = relationship("Participant", foreign_keys=[participant_1_id], lazy="selectin")
    participant_2 = relationship("Participant", foreign_keys=[participant_2_id], lazy="selectin")
