from fastapi_users.db import SQLAlchemyBaseOAuthAccountTableUUID, SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    oauth_accounts = relationship("OAuthAccount", lazy="joined")
    championships = relationship("Championship", back_populates="owner", lazy="selectin")
    participants = relationship("Participant", back_populates="user", lazy="selectin")
