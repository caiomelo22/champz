import uuid

from fastapi_users.db import SQLAlchemyBaseOAuthAccountTableUUID, SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    championships = relationship("Championship", back_populates="owner", lazy="selectin")
