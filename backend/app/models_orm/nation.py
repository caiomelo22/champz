from sqlalchemy import Column, String

from app.db.base import Base


class Nation(Base):
    __tablename__ = "nation"

    name = Column(String(255), primary_key=True)
    image_path = Column(String(512), nullable=False)
