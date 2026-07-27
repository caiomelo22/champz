from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class DraftPick(Base):
    __tablename__ = "draft_pick"

    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(Integer, ForeignKey("participant.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(String(255), ForeignKey("player.id", ondelete="CASCADE"), nullable=False)
    value = Column(Integer, nullable=False)

    participant = relationship("Participant", back_populates="draft_picks")
    player = relationship("Player", lazy="selectin")
