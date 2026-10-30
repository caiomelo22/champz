from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.users import current_active_user
from app.db.base import get_async_session
from app.models.match import UpdateMatchModel
from app.models_orm.match import Match
from app.models_orm.user import User

router = APIRouter()


@router.patch("/update/{match_id}")
async def update_match(
    match_id: int,
    data: UpdateMatchModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Match).where(Match.id == match_id)
    match = (await session.execute(stmt)).scalar_one_or_none()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found.")

    match.goals_1 = data.goals_1
    match.goals_2 = data.goals_2
    match.penalties = data.penalties

    await session.commit()
    return {"detail": "Match updated."}
