import os
import uuid
import logging
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_async_session
from app.models_orm.user import OAuthAccount, User
from app.auth.email import send_verification_email
from app.services.participant_link import resolve_pending_participant_links

SECRET = os.getenv("JWT_SECRET", "CHANGE-ME-IN-PRODUCTION")
VERIFY_SECRET = os.getenv("VERIFY_SECRET", SECRET)
logger = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = VERIFY_SECRET
    verification_token_lifetime_seconds = 60 * 60 * 24

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        if user.is_verified:
            await resolve_pending_participant_links(user.id, user.email)
            return

        try:
            await self.request_verify(user, request)
        except Exception:
            logger.exception("Could not send the verification email for user %s", user.id)

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
        await send_verification_email(user.email, token)

    async def on_after_verify(self, user: User, request: Optional[Request] = None):
        await resolve_pending_participant_links(user.id, user.email)

    async def oauth_callback(
        self,
        oauth_name: str,
        access_token: str,
        account_id: str,
        account_email: str,
        expires_at: Optional[int] = None,
        refresh_token: Optional[str] = None,
        request: Optional[Request] = None,
        *,
        associate_by_email: bool = False,
        is_verified_by_default: bool = False,
    ) -> User:
        user = await super().oauth_callback(
            oauth_name=oauth_name,
            access_token=access_token,
            account_id=account_id,
            account_email=account_email,
            expires_at=expires_at,
            refresh_token=refresh_token,
            request=request,
            associate_by_email=associate_by_email,
            is_verified_by_default=is_verified_by_default,
        )
        if is_verified_by_default and not user.is_verified:
            user = await self.user_db.update(user, {"is_verified": True})
            await self.on_after_verify(user, request)
        return user


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600 * 24)  # 24 hours


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True, verified=True)
current_verified_user = current_active_user
optional_current_user = fastapi_users.current_user(active=True, optional=True)
