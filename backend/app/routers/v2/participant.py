import typing as t

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.users import current_active_user
from app.db.base import get_async_session
from app.models_orm.championship import Championship
from app.models_orm.draft_pick import DraftPick
from app.models_orm.participant import Participant
from app.models_orm.team import Team
from app.models_orm.user import User

router = APIRouter()


class ManageParticipantModel(BaseModel):
    team: str
    name: str
    budget: int


class ParticipantResponse(BaseModel):
    id: int
    name: str
    budget: int
    team_name: t.Optional[str] = None
    team_image_path: t.Optional[str] = None

    class Config:
        from_attributes = True


def _participant_to_response(p: Participant) -> ParticipantResponse:
    return ParticipantResponse(
        id=p.id,
        name=p.name,
        budget=p.budget,
        team_name=p.team.name if p.team else None,
        team_image_path=p.team.image_path if p.team else None,
    )


@router.get("/{championship_id}/participant/list", response_model=t.List[ParticipantResponse])
async def list_participants(
    championship_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    champ_stmt = select(Championship).where(
        Championship.id == championship_id, Championship.owner_id == str(user.id)
    )
    champ = (await session.execute(champ_stmt)).scalar_one_or_none()
    if not champ:
        raise HTTPException(status_code=404, detail="Championship not found.")

    stmt = (
        select(Participant)
        .options(selectinload(Participant.team))
        .where(Participant.championship_id == championship_id)
    )
    result = await session.execute(stmt)
    participants = result.scalars().all()

    return [_participant_to_response(p) for p in participants]


@router.post("/{championship_id}/participant/create", response_model=ParticipantResponse)
async def create_participant(
    championship_id: int,
    data: ManageParticipantModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    champ_stmt = select(Championship).where(
        Championship.id == championship_id, Championship.owner_id == str(user.id)
    )
    champ = (await session.execute(champ_stmt)).scalar_one_or_none()
    if not champ:
        raise HTTPException(status_code=404, detail="Championship not found.")

    # Check team exists
    team_stmt = select(Team).where(Team.name == data.team)
    team = (await session.execute(team_stmt)).scalar_one_or_none()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found.")

    # Check team not already used in this championship
    existing = (
        await session.execute(
            select(Participant).where(
                Participant.championship_id == championship_id,
                Participant.team_name == data.team,
            )
        )
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="The chosen team has already been assigned to another participant.")

    participant = Participant(
        name=data.name,
        budget=data.budget,
        team_name=data.team,
        championship_id=championship_id,
    )
    session.add(participant)
    await session.commit()
    await session.refresh(participant, ["team"])

    return _participant_to_response(participant)


@router.patch("/{championship_id}/participant/update/{participant_id}", response_model=ParticipantResponse)
async def update_participant(
    championship_id: int,
    participant_id: int,
    data: ManageParticipantModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    champ_stmt = select(Championship).where(
        Championship.id == championship_id, Championship.owner_id == str(user.id)
    )
    champ = (await session.execute(champ_stmt)).scalar_one_or_none()
    if not champ:
        raise HTTPException(status_code=404, detail="Championship not found.")

    stmt = (
        select(Participant)
        .options(selectinload(Participant.team))
        .where(Participant.id == participant_id, Participant.championship_id == championship_id)
    )
    participant = (await session.execute(stmt)).scalar_one_or_none()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    # Check team availability if changing team
    if data.team != participant.team_name:
        existing = (
            await session.execute(
                select(Participant).where(
                    Participant.championship_id == championship_id,
                    Participant.team_name == data.team,
                )
            )
        ).scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="The chosen team has already been assigned to another participant.")

        # Check team exists
        team_stmt = select(Team).where(Team.name == data.team)
        team = (await session.execute(team_stmt)).scalar_one_or_none()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found.")

        participant.team_name = data.team

    participant.name = data.name
    participant.budget = data.budget

    await session.commit()
    await session.refresh(participant, ["team"])

    return _participant_to_response(participant)


@router.delete("/{championship_id}/participant/delete/{participant_id}")
async def delete_participant(
    championship_id: int,
    participant_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    champ_stmt = select(Championship).where(
        Championship.id == championship_id, Championship.owner_id == str(user.id)
    )
    champ = (await session.execute(champ_stmt)).scalar_one_or_none()
    if not champ:
        raise HTTPException(status_code=404, detail="Championship not found.")

    stmt = select(Participant).where(
        Participant.id == participant_id, Participant.championship_id == championship_id
    )
    participant = (await session.execute(stmt)).scalar_one_or_none()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    # Draft picks cascade-deleted automatically
    await session.delete(participant)
    await session.commit()
    return {"detail": "Participant deleted."}
