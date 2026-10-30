import typing as t

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.users import current_active_user
from app.db.base import get_async_session
from app.models.position import PositionResponse
from app.models_orm.position import Position
from app.models_orm.user import User

router = APIRouter()


@router.get("/list", response_model=t.List[PositionResponse])
async def list_positions(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(Position))
    positions = result.scalars().all()
    return [PositionResponse.model_validate(p) for p in positions]
