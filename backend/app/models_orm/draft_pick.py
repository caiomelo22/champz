from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class DraftPick(Base):
    __tablename__ = "draft_pick"
    __table_args__ = (
        UniqueConstraint("championship_id", "player_id", name="uq_draft_pick_championship_player"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    championship_id = Column(Integer, ForeignKey("championship.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participant.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(String(255), ForeignKey("player.id", ondelete="CASCADE"), nullable=False)
    value = Column(Integer, nullable=False)

    championship = relationship("Championship", back_populates="draft_picks")
    participant = relationship("Participant", back_populates="draft_picks")
    player = relationship("Player", lazy="selectin")
