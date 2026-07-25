# app/main.py

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.google import google_oauth_client
from app.auth.users import auth_backend, fastapi_users, get_user_manager, get_user_db, get_jwt_strategy, UserManager
from app.db.base import engine, Base, get_async_session
from app.models_orm import *  # noqa: F401,F403 – register all ORM models
from app.models_orm.user import OAuthAccount, User
from fastapi_users.db import SQLAlchemyUserDatabase
from app.routers import group, match, participant, player, position, team
from app.routers.v2 import player as player_v2
from app.routers.v2 import participant as participant_v2
from app.routers.v2 import team as team_v2
from app.routers.v2 import position as position_v2
from app.routers.v2 import match as match_v2
from app.routers.v2 import group as group_v2
from app.routers.championship import router as championship_router
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate

import uuid


class UserRead(BaseUser[uuid.UUID]):
    pass


class UserCreate(BaseUserCreate):
    pass


class UserUpdate(BaseUserUpdate):
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (for development; use alembic in production)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure CORS settings
origins = [
    "http://localhost:8080",  # Add your frontend's origin here
    "http://localhost:3000",
    # Other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Auth routes ──────────────────────────────────────────────
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        "GOOGLE-SECRET",
        associate_by_email=True,
        is_verified_by_default=True,
        redirect_url="http://localhost:8000/auth/google/callback",
    ),
    prefix="/auth/google",
    tags=["auth"],
)

GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google/redirect-callback"
FRONTEND_LOGIN_URL = "http://localhost:8080/login"


@app.get("/auth/google/login")
async def google_login_redirect():
    """Redirect to Google OAuth consent screen."""
    authorization_url = await google_oauth_client.get_authorization_url(
        redirect_uri=GOOGLE_REDIRECT_URI,
        scope=["openid", "email", "profile"],
    )
    return RedirectResponse(authorization_url)


@app.get("/auth/google/redirect-callback")
async def google_redirect_callback(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Handle Google callback, generate JWT, and redirect to frontend."""
    code = request.query_params.get("code")
    token_data = await google_oauth_client.get_access_token(code, GOOGLE_REDIRECT_URI)
    account_id, account_email = await google_oauth_client.get_id_email(
        token_data["access_token"]
    )

    user_db = SQLAlchemyUserDatabase(session, User, OAuthAccount)
    user_manager = UserManager(user_db)

    user = await user_manager.oauth_callback(
        oauth_name="google",
        access_token=token_data["access_token"],
        account_id=account_id,
        account_email=account_email,
        expires_at=token_data.get("expires_at"),
        refresh_token=token_data.get("refresh_token"),
        request=request,
        associate_by_email=True,
        is_verified_by_default=True,
    )

    jwt_strategy = get_jwt_strategy()
    jwt_token = await jwt_strategy.write_token(user)

    return RedirectResponse(f"{FRONTEND_LOGIN_URL}?token={jwt_token}")

# ── Championship routes (new, scoped) ───────────────────────
app.include_router(championship_router, prefix="/championship", tags=["championship"])

# ── V2 routes (championship-scoped, SQLAlchemy) ─────────────
app.include_router(player_v2.router, prefix="/championship", tags=["player"])
app.include_router(participant_v2.router, prefix="/championship", tags=["participant"])
app.include_router(team_v2.router, prefix="/team", tags=["team"])
app.include_router(position_v2.router, prefix="/position", tags=["position"])
app.include_router(match_v2.router, prefix="/match", tags=["match"])
app.include_router(group_v2.router, prefix="/championship", tags=["group"])

# ── Legacy routes (kept for backward compatibility) ─────────
app.include_router(player.router, prefix="/legacy/player", tags=["legacy"])
app.include_router(position.router, prefix="/legacy/position", tags=["legacy"])
app.include_router(team.router, prefix="/legacy/team", tags=["legacy"])
app.include_router(participant.router, prefix="/legacy/participant", tags=["legacy"])
app.include_router(match.router, prefix="/legacy/match", tags=["legacy"])
app.include_router(group.router, prefix="/legacy/group", tags=["legacy"])
