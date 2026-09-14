from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class PlayerAuction(Base):
    __tablename__ = "player_auction"
    __table_args__ = (
        UniqueConstraint("championship_id", "player_id", name="uq_player_auction_championship_player"),
        Index("ix_player_auction_status_deadline", "status", "deadline"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    championship_id = Column(Integer, ForeignKey("championship.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(String(255), ForeignKey("player.id", ondelete="CASCADE"), nullable=False)
    deadline = Column(DateTime, nullable=False)
    minimum_bid = Column(Integer, nullable=False)
    status = Column(
        Enum("open", "closed", "cancelled", name="player_auction_status"),
        default="open",
        nullable=False,
    )
    leading_participant_id = Column(
        Integer,
        ForeignKey("participant.id", ondelete="SET NULL"),
        nullable=True,
    )
    leading_bid = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    championship = relationship("Championship", back_populates="auctions")
    player = relationship("Player", lazy="selectin")
    leading_participant = relationship(
        "Participant",
        back_populates="leading_auctions",
        foreign_keys=[leading_participant_id],
        lazy="selectin",
    )
    bids = relationship("Bid", back_populates="auction", cascade="all, delete-orphan", lazy="selectin")