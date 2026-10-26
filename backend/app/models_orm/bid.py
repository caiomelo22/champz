from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Bid(Base):
    __tablename__ = "bid"
    __table_args__ = (
        Index("ix_bid_auction_created_at", "auction_id", "created_at"),
        Index("ix_bid_participant", "participant_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    auction_id = Column(Integer, ForeignKey("player_auction.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participant.id", ondelete="RESTRICT"), nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    auction = relationship("PlayerAuction", back_populates="bids")
    participant = relationship("Participant", back_populates="bids")