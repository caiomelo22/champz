import typing as t

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.users import current_active_user
from app.db.base import get_async_session
from app.models_orm.player import Player
from app.models_orm.team import Team
from app.models_orm.user import User

router = APIRouter()


class TeamResponse(BaseModel):
    name: str
    image_path: str

    class Config:
        from_attributes = True


@router.get("/most-popular", response_model=t.List[TeamResponse])
async def most_popular(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = (
        select(Team, func.count(Player.id).label("n_players"))
        .join(Player, Player.team_origin == Team.name)
        .group_by(Team.name)
        .order_by(func.count(Player.id).desc())
        .limit(40)
    )
    result = await session.execute(stmt)
    rows = result.all()

    return [TeamResponse(name=t.name, image_path=t.image_path) for t, _ in rows]
