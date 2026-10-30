from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.base import Base


class ChampionshipPlayer(Base):
    """Player selected by the championship owner to take part in the draft."""

    __tablename__ = "championship_player"

    championship_id = Column(Integer, ForeignKey("championship.id", ondelete="CASCADE"), primary_key=True)
    player_id = Column(String(255), ForeignKey("player.id", ondelete="CASCADE"), primary_key=True)
