import typing as t
from io import BytesIO

import openpyxl
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.users import current_active_user
from app.db.base import get_async_session
from app.dependencies.championship import get_championship_access, require_owner
from app.models.player import BuyPlayerModel, PlayerResponse, PoolPlayerResponse, PoolResponse, UpdatePoolModel
from app.models_orm.championship import Championship
from app.models_orm.draft_pick import DraftPick
from app.models_orm.participant import Participant
from app.models_orm.player import Player
from app.models_orm.position import Position
from app.models_orm.user import User
from app.models_orm.player_auction import PlayerAuction
from app.services.draft_pool import (
    ensure_in_pool,
    get_locked_player_ids,
    get_pool_player_ids,
    pool_player_ids_stmt,
    replace_pool,
    suggest_player_ids,
)
from app.utils.export import write_players_sheet

router = APIRouter()


def _player_to_response(player: Player, draft_pick: t.Optional[DraftPick] = None, participant: t.Optional[Participant] = None) -> PlayerResponse:
    team_participant = None
    team_participant_name = None
    team_participant_image_path = None
    participant_id = None
    value = None

    if draft_pick and participant:
        team_participant = participant.team_name
        if participant.team:
            team_participant_name = participant.team.name
            team_participant_image_path = participant.team.image_path
        participant_id = participant.id
        value = draft_pick.value

    return PlayerResponse(
        id=player.id,
        position_id=player.position_id,
        position_name=player.position.name if player.position else "",
        team_participant=team_participant,
        team_participant_name=team_participant_name,
        team_participant_image_path=team_participant_image_path,
        participant_id=participant_id,
        team_origin=player.team_origin,
        team_origin_name=player.team_origin_rel.name if player.team_origin_rel else player.team_origin,
        team_origin_image_path=player.team_origin_rel.image_path if player.team_origin_rel else "",
        name=player.name,
        nation=player.nation,
        nation_name=player.nation_rel.name if player.nation_rel else player.nation,
        nation_image_path=player.nation_rel.image_path if player.nation_rel else "",
        specific_position=player.specific_position,
        overall=player.overall,
        pace=player.pace,
        shooting=player.shooting,
        passing=player.passing,
        dribbling=player.dribbling,
        defending=player.defending,
        physical=player.physical,
        image_path=player.image_path,
        value=value,
    )


def _players_stmt():
    return select(Player).options(
        selectinload(Player.position),
        selectinload(Player.team_origin_rel),
        selectinload(Player.nation_rel),
    ).order_by(Player.position_id, Player.overall.desc(), Player.pace.desc())


@router.get("/player/catalog", response_model=t.List[PoolPlayerResponse])
async def player_catalog(
    num_participants: int = Query(0, ge=0, description="Expected participants, used to pre-select the draft pool"),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """All players available for a new championship, with the suggested draft pool selected."""
    players = (await session.execute(_players_stmt())).scalars().all()
    suggested = await suggest_player_ids(session, num_participants)
    return [
        PoolPlayerResponse(**_player_to_response(p).model_dump(), selected=p.id in suggested)
        for p in players
    ]


@router.get("/{championship_id}/player/pool", response_model=t.List[PoolPlayerResponse])
async def get_player_pool(
    championship_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)

    players = (await session.execute(_players_stmt())).scalars().all()
    pool = await get_pool_player_ids(session, championship_id)
    locked = await get_locked_player_ids(session, championship_id)
    draft_pick_by_player = {
        draft_pick.player_id: draft_pick
        for draft_pick in (
            await session.execute(
                select(DraftPick)
                .where(DraftPick.championship_id == championship_id)
                .options(selectinload(DraftPick.participant).selectinload(Participant.team))
            )
        ).scalars().all()
    }

    responses = []
    for p in players:
        draft_pick = draft_pick_by_player.get(p.id)
        response = _player_to_response(p, draft_pick, draft_pick.participant if draft_pick else None)
        responses.append(PoolPlayerResponse(**response.model_dump(), selected=p.id in pool, locked=p.id in locked))
    return responses


@router.put("/{championship_id}/player/pool", response_model=PoolResponse)
async def update_player_pool(
    championship_id: int,
    data: UpdatePoolModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)

    player_ids = await replace_pool(session, championship_id, data.player_ids)
    await session.commit()
    return PoolResponse(player_ids=sorted(player_ids))


@router.get("/{championship_id}/player/list", response_model=t.List[PlayerResponse])
async def list_players(
    championship_id: int,
    position: t.Optional[int] = Query(None, description="Filter by position ID"),
    participant_id: t.Optional[int] = Query(None, description="Filter by participant (drafted players)"),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    await get_championship_access(session, championship_id, user)

    stmt = _players_stmt()
    if position:
        stmt = stmt.where(Player.position_id == position)

    # A participant's team is always listed in full; otherwise only the draft pool
    if not participant_id:
        stmt = stmt.where(Player.id.in_(pool_player_ids_stmt(championship_id)))

    result = await session.execute(stmt)
    players = result.scalars().all()

    # Get all draft picks for this championship
    draft_picks_stmt = (
        select(DraftPick)
        .join(Participant, DraftPick.participant_id == Participant.id)
        .where(Participant.championship_id == championship_id)
        .options(selectinload(DraftPick.participant).selectinload(Participant.team))
    )
    if participant_id:
        draft_picks_stmt = draft_picks_stmt.where(DraftPick.participant_id == participant_id)

    draft_picks_result = await session.execute(draft_picks_stmt)
    draft_picks = draft_picks_result.scalars().all()

    # Build lookup: player_id -> (draft_pick, participant)
    draft_pick_by_player = {}
    for draft_pick in draft_picks:
        draft_pick_by_player[draft_pick.player_id] = (draft_pick, draft_pick.participant)

    responses = []
    for p in players:
        draft_pick_info = draft_pick_by_player.get(p.id)
        if participant_id and not draft_pick_info:
            continue  # Filter: only show this participant's players
        draft_pick = draft_pick_info[0] if draft_pick_info else None
        participant = draft_pick_info[1] if draft_pick_info else None
        responses.append(_player_to_response(p, draft_pick, participant))

    return responses


@router.post("/{championship_id}/player/buy/{player_id}", response_model=PlayerResponse)
async def buy_player(
    championship_id: int,
    player_id: str,
    data: BuyPlayerModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)

    await session.execute(
        select(Championship.id)
        .where(Championship.id == championship_id)
        .with_for_update()
    )

    auction = (
        await session.execute(
            select(PlayerAuction).where(
                PlayerAuction.championship_id == championship_id,
                PlayerAuction.player_id == player_id,
            )
        )
    ).scalar_one_or_none()
    if auction and auction.status != "cancelled":
        raise HTTPException(
            status_code=409,
            detail="Players with an active or completed auction cannot be assigned manually.",
        )
    if data.participant_id:
        await ensure_in_pool(session, championship_id, [player_id])

    # Get the player
    player_stmt = select(Player).options(
        selectinload(Player.position),
        selectinload(Player.team_origin_rel),
        selectinload(Player.nation_rel),
    ).where(Player.id == player_id)
    player = (await session.execute(player_stmt)).scalar_one_or_none()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found.")

    # Check if player is already drafted in this championship
    existing_draft_pick_stmt = (
        select(DraftPick)
        .join(Participant, DraftPick.participant_id == Participant.id)
        .where(
            Participant.championship_id == championship_id,
            DraftPick.player_id == player_id,
        )
        .options(selectinload(DraftPick.participant).selectinload(Participant.team))
        .with_for_update()
    )
    existing_draft_pick = (await session.execute(existing_draft_pick_stmt)).scalar_one_or_none()

    participant_ids = {
        participant_id
        for participant_id in (
            existing_draft_pick.participant_id if existing_draft_pick else None,
            data.participant_id,
        )
        if participant_id is not None
    }
    participants = (
        await session.execute(
            select(Participant)
            .options(selectinload(Participant.team))
            .where(
                Participant.championship_id == championship_id,
                Participant.id.in_(sorted(participant_ids)),
            )
            .order_by(Participant.id)
            .with_for_update()
        )
    ).scalars().all()
    participant_by_id = {participant.id: participant for participant in participants}

    # If player already drafted, refund and remove
    if existing_draft_pick:
        old_participant = participant_by_id[existing_draft_pick.participant_id]
        old_participant.budget += existing_draft_pick.value
        await session.delete(existing_draft_pick)
        await session.flush()

    # If no new participant specified, just undraft
    if not data.participant_id:
        await session.commit()
        return _player_to_response(player)

    if not data.value:
        raise HTTPException(status_code=400, detail="Player value not valid.")

    new_participant = participant_by_id.get(data.participant_id)
    if not new_participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    if new_participant.budget < data.value:
        raise HTTPException(status_code=400, detail="Participant does not have enough budget.")

    # Create draft pick and deduct budget
    new_participant.budget -= data.value
    new_draft_pick = DraftPick(
        championship_id=championship_id,
        participant_id=new_participant.id,
        player_id=player_id,
        value=data.value,
    )
    session.add(new_draft_pick)
    await session.commit()

    return _player_to_response(player, new_draft_pick, new_participant)


@router.get("/{championship_id}/player/sheet")
async def get_sheet(
    championship_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)

    positions_result = await session.execute(select(Position))
    positions = positions_result.scalars().all()

    wb = openpyxl.Workbook()

    for i, pos in enumerate(positions):
        wb.create_sheet(index=i, title=pos.name)
        wb.active = i

        stmt = _players_stmt().where(
            Player.position_id == pos.id,
            Player.id.in_(pool_player_ids_stmt(championship_id)),
        )

        result = await session.execute(stmt)
        players = result.scalars().all()

        # Get draft picks for this championship
        draft_picks_stmt = (
            select(DraftPick)
            .join(Participant).where(Participant.championship_id == championship_id)
            .options(selectinload(DraftPick.participant))
        )
        draft_picks_result = await session.execute(draft_picks_stmt)
        draft_pick_by_player = {draft_pick.player_id: draft_pick for draft_pick in draft_picks_result.scalars().all()}

        player_responses = []
        for p in players:
            draft_pick = draft_pick_by_player.get(p.id)
            participant = draft_pick.participant if draft_pick else None
            player_responses.append(_player_to_response(p, draft_pick, participant))

        write_players_sheet(wb.active, player_responses)

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)

    return Response(
        content=stream.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=sheet.xlsx"},
    )
