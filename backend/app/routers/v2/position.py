import typing as t

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.users import current_active_user
from app.db.base import get_async_session
from app.models_orm.position import Position
from app.models_orm.user import User

router = APIRouter()


class PositionResponse(BaseModel):
    id: int
    name: str
    specific_positions: str

    class Config:
        from_attributes = True


@router.get("/list", response_model=t.List[PositionResponse])
async def list_positions(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(Position))
    positions = result.scalars().all()
    return [PositionResponse.model_validate(p) for p in positions]
