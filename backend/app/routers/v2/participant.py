import typing as t

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.users import current_active_user
from app.db.base import get_async_session
from app.dependencies.championship import get_championship_access, require_owner
from app.models_orm.bid import Bid
from app.models_orm.championship import Championship
from app.models_orm.draft_pick import DraftPick
from app.models_orm.participant import Participant
from app.models_orm.player_auction import PlayerAuction
from app.models_orm.team import Team
from app.models_orm.user import User
from app.services.participant_link import normalize_email

router = APIRouter()


class ManageParticipantModel(BaseModel):
    team: str
    name: str
    budget: int = Field(ge=0)
    user_email: t.Optional[str] = None


class ParticipantResponse(BaseModel):
    id: int
    name: str
    budget: t.Optional[int] = None
    team_name: t.Optional[str] = None
    team_image_path: t.Optional[str] = None
    user_email: t.Optional[str] = None
    link_status: str = "unlinked"

    class Config:
        from_attributes = True


def _participant_to_response(
    p: Participant,
    include_budget: bool = True,
    include_user_email: bool = False,
) -> ParticipantResponse:
    user_email = None
    link_status = "unlinked"
    if p.user_id:
        link_status = "linked"
        if include_user_email and p.user:
            user_email = p.user.email
    elif p.pending_user_email:
        link_status = "pending"
        if include_user_email:
            user_email = p.pending_user_email

    return ParticipantResponse(
        id=p.id,
        name=p.name,
        budget=p.budget if include_budget else None,
        team_name=p.team.name if p.team else None,
        team_image_path=p.team.image_path if p.team else None,
        user_email=user_email,
        link_status=link_status,
    )


async def _resolve_user_link(
    session: AsyncSession,
    championship_id: int,
    user_email: t.Optional[str],
    participant_id: t.Optional[int] = None,
) -> tuple[t.Optional[str], t.Optional[str]]:
    if not user_email or not user_email.strip():
        return None, None

    normalized_email = normalize_email(user_email)
    linked_user = (
        await session.execute(select(User).where(func.lower(User.email) == normalized_email))
    ).unique().scalar_one_or_none()
    user_id = linked_user.id if linked_user and linked_user.is_active and linked_user.is_verified else None
    pending_email = None if user_id else normalized_email

    duplicate_stmt = select(Participant.id).where(Participant.championship_id == championship_id)
    if participant_id is not None:
        duplicate_stmt = duplicate_stmt.where(Participant.id != participant_id)
    if user_id:
        duplicate_stmt = duplicate_stmt.where(Participant.user_id == user_id)
    else:
        duplicate_stmt = duplicate_stmt.where(Participant.pending_user_email == pending_email)
    if (await session.execute(duplicate_stmt)).scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="This account is already linked or pending in the championship.",
        )

    return user_id, pending_email


@router.get("/{championship_id}/participant/list", response_model=t.List[ParticipantResponse])
async def list_participants(
    championship_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)

    stmt = (
        select(Participant)
        .options(selectinload(Participant.team), selectinload(Participant.user))
        .where(Participant.championship_id == championship_id)
    )
    result = await session.execute(stmt)
    participants = result.scalars().all()

    return [
        _participant_to_response(
            participant,
            include_budget=(
                access.role == "owner"
                or (access.participant is not None and access.participant.id == participant.id)
            ),
            include_user_email=access.role == "owner",
        )
        for participant in participants
    ]


@router.post("/{championship_id}/participant/create", response_model=ParticipantResponse)
async def create_participant(
    championship_id: int,
    data: ManageParticipantModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)

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

    user_id, pending_user_email = await _resolve_user_link(
        session,
        championship_id,
        data.user_email,
    )
    participant = Participant(
        name=data.name,
        budget=data.budget,
        team_name=data.team,
        championship_id=championship_id,
        user_id=user_id,
        pending_user_email=pending_user_email,
    )
    session.add(participant)
    await session.commit()
    await session.refresh(participant, ["team", "user"])

    return _participant_to_response(participant, include_user_email=True)


@router.patch("/{championship_id}/participant/update/{participant_id}", response_model=ParticipantResponse)
async def update_participant(
    championship_id: int,
    participant_id: int,
    data: ManageParticipantModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)

    stmt = (
        select(Participant)
        .options(selectinload(Participant.team), selectinload(Participant.user))
        .where(Participant.id == participant_id, Participant.championship_id == championship_id)
        .with_for_update()
    )
    participant = (await session.execute(stmt)).scalar_one_or_none()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    if data.budget != participant.budget:
        leads_open_auction = (
            await session.execute(
                select(PlayerAuction.id)
                .where(
                    PlayerAuction.leading_participant_id == participant.id,
                    PlayerAuction.status == "open",
                )
                .limit(1)
            )
        ).scalar_one_or_none()
        if leads_open_auction is not None:
            raise HTTPException(
                status_code=409,
                detail="Budget cannot be changed while the participant leads an open auction.",
            )

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
    participant.user_id, participant.pending_user_email = await _resolve_user_link(
        session,
        championship_id,
        data.user_email,
        participant_id=participant.id,
    )

    await session.commit()
    await session.refresh(participant, ["team", "user"])

    return _participant_to_response(participant, include_user_email=True)


@router.delete("/{championship_id}/participant/delete/{participant_id}")
async def delete_participant(
    championship_id: int,
    participant_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)

    stmt = select(Participant).where(
        Participant.id == participant_id, Participant.championship_id == championship_id
    )
    participant = (await session.execute(stmt)).scalar_one_or_none()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    existing_bid = (
        await session.execute(select(Bid.id).where(Bid.participant_id == participant_id).limit(1))
    ).scalar_one_or_none()
    if existing_bid:
        raise HTTPException(
            status_code=409,
            detail="A participant with bid history cannot be deleted.",
        )

    # Draft picks cascade-deleted automatically
    await session.delete(participant)
    await session.commit()
    return {"detail": "Participant deleted."}
