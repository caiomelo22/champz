import typing as t

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.users import current_active_user
from app.db.base import get_async_session
from app.dependencies.championship import get_championship_access, require_owner
from app.models.championship import ChampionshipResponse, CreateChampionshipModel, UpdateChampionshipModel
from app.models_orm.championship import Championship
from app.models_orm.participant import Participant
from app.models_orm.user import User
from app.models_orm.player_auction import PlayerAuction
from app.services.draft_pool import add_pool_players

router = APIRouter()


@router.post("/create", response_model=ChampionshipResponse)
async def create_championship(
    data: CreateChampionshipModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    championship = Championship(
        name=data.name,
        owner_id=user.id,
        budget_default=data.budget_default,
    )
    session.add(championship)
    await session.flush()
    await add_pool_players(session, championship.id, data.player_ids)
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
    membership_stmt = select(Participant.championship_id, Participant.id).where(
        Participant.user_id == user.id
    )
    membership_rows = (await session.execute(membership_stmt)).all() if user.is_verified else []
    membership_by_championship = {championship_id: participant_id for championship_id, participant_id in membership_rows}
    participant_count = (
        select(func.count(Participant.id))
        .where(Participant.championship_id == Championship.id)
        .correlate(Championship)
        .scalar_subquery()
    )
    accessible_championships_stmt = (
        select(
            Championship,
            participant_count.label("num_participants"),
        )
        .where(
            or_(
                Championship.owner_id == user.id,
                Championship.id.in_(membership_by_championship.keys()),
            )
        )
        .order_by(Championship.updated_at.desc())
    )
    result = await session.execute(accessible_championships_stmt)
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
            access_role="owner" if champ.owner_id == user.id else "participant",
            participant_id=membership_by_championship.get(champ.id),
        )
        for champ, num_p in rows
    ]


@router.get("/{championship_id}", response_model=ChampionshipResponse)
async def get_championship(
    championship_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    num_p = (
        await session.execute(
            select(func.count(Participant.id)).where(Participant.championship_id == championship_id)
        )
    ).scalar_one()
    champ = access.championship
    return ChampionshipResponse(
        id=champ.id,
        name=champ.name,
        status=champ.status,
        budget_default=champ.budget_default,
        created_at=champ.created_at,
        updated_at=champ.updated_at,
        num_participants=num_p,
        access_role=access.role,
        participant_id=access.participant.id if access.participant else None,
    )


@router.put("/{championship_id}", response_model=ChampionshipResponse)
async def update_championship(
    championship_id: int,
    data: UpdateChampionshipModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)
    championship = access.championship

    if data.name is not None:
        championship.name = data.name
    if data.status is not None:
        if data.status not in ("draft", "games", "complete"):
            raise HTTPException(status_code=400, detail="Invalid status.")
        if data.status != "draft":
            open_auction = (
                await session.execute(
                    select(PlayerAuction.id).where(
                        PlayerAuction.championship_id == championship_id,
                        PlayerAuction.status == "open",
                    ).limit(1)
                )
            ).scalar_one_or_none()
            if open_auction:
                raise HTTPException(
                    status_code=409,
                    detail="Open auctions must be closed or cancelled first.",
                )
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
        access_role="owner",
        participant_id=access.participant.id if access.participant else None,
    )


@router.delete("/{championship_id}")
async def delete_championship(
    championship_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)
    championship = access.championship

    await session.delete(championship)
    await session.commit()
    return {"detail": "Championship deleted."}
