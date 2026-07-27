from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Position(Base):
    __tablename__ = "position"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    specific_positions = Column(String(255), nullable=False)
