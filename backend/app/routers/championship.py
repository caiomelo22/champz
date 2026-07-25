import typing as t
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.users import current_active_user
from app.db.base import get_async_session
from app.models_orm.championship import Championship
from app.models_orm.group import Group
from app.models_orm.match import Match
from app.models_orm.participant import Participant
from app.models_orm.user import User

router = APIRouter()


class CreateChampionshipModel(BaseModel):
    name: str
    budget_default: int = 250


class UpdateChampionshipModel(BaseModel):
    name: t.Optional[str] = None
    status: t.Optional[str] = None


class ChampionshipResponse(BaseModel):
    id: int
    name: str
    status: str
    budget_default: int
    created_at: datetime
    updated_at: datetime
    num_participants: int = 0

    class Config:
        from_attributes = True


@router.post("/create", response_model=ChampionshipResponse)
async def create_championship(
    data: CreateChampionshipModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    championship = Championship(
        name=data.name,
        owner_id=str(user.id),
        budget_default=data.budget_default,
    )
    session.add(championship)
    await session.commit()
    await session.refresh(championship)

    return ChampionshipResponse(
        id=championship.id,
        name=championship.name,
        status=championship.status,
        budget_default=championship.budget_default,
        created_at=championship.created_at,
        updated_at=championship.updated_at,
        num_participants=0,
    )


@router.get("/list", response_model=t.List[ChampionshipResponse])
async def list_championships(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = (
        select(
            Championship,
            func.count(Participant.id).label("num_participants"),
        )
        .outerjoin(Participant, Participant.championship_id == Championship.id)
        .where(Championship.owner_id == str(user.id))
        .group_by(Championship.id)
        .order_by(Championship.updated_at.desc())
    )
    result = await session.execute(stmt)
    rows = result.all()

    return [
        ChampionshipResponse(
            id=champ.id,
            name=champ.name,
            status=champ.status,
            budget_default=champ.budget_default,
            created_at=champ.created_at,
            updated_at=champ.updated_at,
            num_participants=num_p,
        )
        for champ, num_p in rows
    ]


@router.get("/{championship_id}", response_model=ChampionshipResponse)
async def get_championship(
    championship_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = (
        select(
            Championship,
            func.count(Participant.id).label("num_participants"),
        )
        .outerjoin(Participant, Participant.championship_id == Championship.id)
        .where(Championship.id == championship_id, Championship.owner_id == str(user.id))
        .group_by(Championship.id)
    )
    result = await session.execute(stmt)
    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Championship not found.")

    champ, num_p = row
    return ChampionshipResponse(
        id=champ.id,
        name=champ.name,
        status=champ.status,
        budget_default=champ.budget_default,
        created_at=champ.created_at,
        updated_at=champ.updated_at,
        num_participants=num_p,
    )


@router.put("/{championship_id}", response_model=ChampionshipResponse)
async def update_championship(
    championship_id: int,
    data: UpdateChampionshipModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Championship).where(
        Championship.id == championship_id, Championship.owner_id == str(user.id)
    )
    result = await session.execute(stmt)
    championship = result.scalar_one_or_none()

    if not championship:
        raise HTTPException(status_code=404, detail="Championship not found.")

    if data.name is not None:
        championship.name = data.name
    if data.status is not None:
        if data.status not in ("draft", "games", "complete"):
            raise HTTPException(status_code=400, detail="Invalid status.")
        championship.status = data.status

    await session.commit()
    await session.refresh(championship)

    num_p = len(championship.participants) if championship.participants else 0
    return ChampionshipResponse(
        id=championship.id,
        name=championship.name,
        status=championship.status,
        budget_default=championship.budget_default,
        created_at=championship.created_at,
        updated_at=championship.updated_at,
        num_participants=num_p,
    )


@router.delete("/{championship_id}")
async def delete_championship(
    championship_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Championship).where(
        Championship.id == championship_id, Championship.owner_id == str(user.id)
    )
    result = await session.execute(stmt)
    championship = result.scalar_one_or_none()

    if not championship:
        raise HTTPException(status_code=404, detail="Championship not found.")

    await session.delete(championship)
    await session.commit()
    return {"detail": "Championship deleted."}
