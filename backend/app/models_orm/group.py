from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    championship_id = Column(Integer, ForeignKey("championship.id", ondelete="CASCADE"), nullable=False)

    championship = relationship("Championship", back_populates="groups")
    group_participants = relationship("GroupParticipant", back_populates="group", cascade="all, delete-orphan", lazy="selectin")
    matches = relationship("Match", back_populates="group", cascade="all, delete-orphan", lazy="selectin")


class GroupParticipant(Base):
    __tablename__ = "group_participant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("group.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participant.id", ondelete="CASCADE"), nullable=False)

    group = relationship("Group", back_populates="group_participants")
    participant = relationship("Participant", lazy="selectin")
