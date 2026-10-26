from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class Participant(Base):
    __tablename__ = "participant"
    __table_args__ = (
        UniqueConstraint("championship_id", "user_id", name="uq_participant_championship_user"),
        UniqueConstraint(
            "championship_id",
            "pending_user_email",
            name="uq_participant_championship_pending_email",
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    budget = Column(Integer, nullable=False)
    team_name = Column(String(255), ForeignKey("team.name", ondelete="SET NULL"), nullable=True)
    championship_id = Column(Integer, ForeignKey("championship.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(GUID, ForeignKey("user.id", ondelete="SET NULL"), nullable=True, index=True)
    pending_user_email = Column(String(320), nullable=True, index=True)

    championship = relationship("Championship", back_populates="participants")
    user = relationship("User", back_populates="participants", lazy="selectin")
    team = relationship("Team", lazy="selectin")
    draft_picks = relationship("DraftPick", back_populates="participant", cascade="all, delete-orphan", lazy="selectin")
    bids = relationship("Bid", back_populates="participant", lazy="selectin")
    leading_auctions = relationship(
        "PlayerAuction",
        back_populates="leading_participant",
        foreign_keys="PlayerAuction.leading_participant_id",
        lazy="selectin",
    )
