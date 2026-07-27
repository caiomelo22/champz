from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Participant(Base):
    __tablename__ = "participant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    budget = Column(Integer, nullable=False)
    team_name = Column(String(255), ForeignKey("team.name", ondelete="SET NULL"), nullable=True)
    championship_id = Column(Integer, ForeignKey("championship.id", ondelete="CASCADE"), nullable=False)

    championship = relationship("Championship", back_populates="participants")
    team = relationship("Team", lazy="selectin")
    draft_picks = relationship("DraftPick", back_populates="participant", cascade="all, delete-orphan", lazy="selectin")
