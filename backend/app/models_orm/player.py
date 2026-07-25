from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Player(Base):
    __tablename__ = "player"

    id = Column(String(255), primary_key=True)
    position_id = Column(Integer, ForeignKey("position.id"), nullable=False)
    team_origin = Column(String(255), ForeignKey("team.name"), nullable=False)
    name = Column(String(255), nullable=False)
    nation = Column(String(255), ForeignKey("nation.name"), nullable=False)
    specific_position = Column(String(10), nullable=False)
    overall = Column(Integer, nullable=False)
    pace = Column(Integer, nullable=False)
    shooting = Column(Integer, nullable=False)
    passing = Column(Integer, nullable=False)
    dribbling = Column(Integer, nullable=False)
    defending = Column(Integer, nullable=False)
    physical = Column(Integer, nullable=False)
    image_path = Column(String(512), nullable=False)

    position = relationship("Position", lazy="selectin")
    team_origin_rel = relationship("Team", foreign_keys=[team_origin], lazy="selectin")
    nation_rel = relationship("Nation", lazy="selectin")
