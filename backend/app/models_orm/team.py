from sqlalchemy import Column, String

from app.db.base import Base


class Team(Base):
    __tablename__ = "team"

    name = Column(String(255), primary_key=True)
    image_path = Column(String(512), nullable=False)
