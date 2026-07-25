import math
import typing as t
from random import shuffle

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select, func, case, and_, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.users import current_active_user
from app.db.base import get_async_session
from app.models_orm.championship import Championship
from app.models_orm.group import Group, GroupParticipant
from app.models_orm.match import Match
from app.models_orm.participant import Participant
from app.models_orm.user import User
from app.utils.helper import get_knockout_info

router = APIRouter()


class GroupResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class GenerateKnockoutModel(BaseModel):
    group_id: int
    previous_round: int


class GroupTableParticipantResponse(BaseModel):
    group_id: int
    participant_id: int
    name: str
    team_image_path: t.Optional[str] = None
    GF: int = 0
    GA: int = 0
    GD: int = 0
    W: int = 0
    L: int = 0
    D: int = 0
    P: int = 0

    class Config:
        from_attributes = True


class MatchResponse(BaseModel):
    id: int
    participant_1_id: int
    participant_2_id: int
    participant_1_name: str
    participant_1_team_name: str
    participant_1_team_image_path: str
    participant_2_name: str
    participant_2_team_name: str
    participant_2_team_image_path: str
    goals_1: t.Optional[int] = None
    goals_2: t.Optional[int] = None
    round: t.Optional[int] = None
    penalties: t.Optional[bool] = False

    class Config:
        from_attributes = True


def _match_to_response(m: Match) -> MatchResponse:
    p1 = m.participant_1
    p2 = m.participant_2
    return MatchResponse(
        id=m.id,
        participant_1_id=m.participant_1_id,
        participant_2_id=m.participant_2_id,
        participant_1_name=p1.name if p1 else "",
        participant_1_team_name=p1.team.name if p1 and p1.team else "",
        participant_1_team_image_path=p1.team.image_path if p1 and p1.team else "",
        participant_2_name=p2.name if p2 else "",
        participant_2_team_name=p2.team.name if p2 and p2.team else "",
        participant_2_team_image_path=p2.team.image_path if p2 and p2.team else "",
        goals_1=m.goals_1,
        goals_2=m.goals_2,
        round=m.round,
        penalties=m.penalties,
    )


async def _get_group_table(session: AsyncSession, group_id: int) -> t.List[GroupTableParticipantResponse]:
    """Calculate the group table from matches."""
    # Get group participants
    gp_stmt = (
        select(GroupParticipant)
        .options(selectinload(GroupParticipant.participant).selectinload(Participant.team))
        .where(GroupParticipant.group_id == group_id)
    )
    gp_result = await session.execute(gp_stmt)
    group_participants = gp_result.scalars().all()

    if not group_participants:
        return []

    # Get the max round for this group (current stage)
    max_round_stmt = select(func.max(Match.round)).where(Match.group_id == group_id)
    max_round = (await session.execute(max_round_stmt)).scalar()

    if max_round is None:
        return []

    # Get all matches for the max round
    matches_stmt = (
        select(Match)
        .where(Match.group_id == group_id, Match.round == max_round)
    )
    matches_result = await session.execute(matches_stmt)
    matches = matches_result.scalars().all()

    # Calculate stats per participant
    table = []
    for gp in group_participants:
        pid = gp.participant_id
        p = gp.participant
        gf = ga = w = l = d = 0

        for m in matches:
            if m.goals_1 is None or m.goals_2 is None:
                continue
            if m.participant_1_id == pid:
                gf += m.goals_1
                ga += m.goals_2
                if m.goals_1 > m.goals_2:
                    w += 1
                elif m.goals_1 < m.goals_2:
                    l += 1
                else:
                    d += 1
            elif m.participant_2_id == pid:
                gf += m.goals_2
                ga += m.goals_1
                if m.goals_2 > m.goals_1:
                    w += 1
                elif m.goals_2 < m.goals_1:
                    l += 1
                else:
                    d += 1

        points = w * 3 + d
        table.append(GroupTableParticipantResponse(
            group_id=group_id,
            participant_id=pid,
            name=p.name,
            team_image_path=p.team.image_path if p.team else None,
            GF=gf,
            GA=ga,
            GD=gf - ga,
            W=w,
            L=l,
            D=d,
            P=points,
        ))

    # Sort by Points DESC, GD DESC, GF DESC
    table.sort(key=lambda x: (-x.P, -x.GD, -x.GF, x.GA))
    return table


@router.post("/{championship_id}/group/create")
async def create_group(
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

    # Get all participants for this championship
    p_stmt = select(Participant).where(Participant.championship_id == championship_id)
    p_result = await session.execute(p_stmt)
    participants = p_result.scalars().all()
    participant_ids = [p.id for p in participants]

    group_name = f"G{len(participant_ids)}"
    group = Group(name=group_name, championship_id=championship_id)
    session.add(group)
    await session.flush()

    for pid in participant_ids:
        gp = GroupParticipant(group_id=group.id, participant_id=pid)
        session.add(gp)

    # Generate group stage matches
    num_participants = len(participant_ids)
    n_games = (num_participants * (num_participants - 1)) / 2

    matches_to_create = []
    for i in range(num_participants):
        for j in range(i + 1, num_participants):
            matches_to_create.append(
                Match(
                    group_id=group.id,
                    participant_1_id=participant_ids[i],
                    participant_2_id=participant_ids[j],
                    round=int(n_games),
                )
            )

    shuffle(matches_to_create)
    session.add_all(matches_to_create)
    await session.commit()

    return group.id


@router.post("/{championship_id}/group/generate-knockout")
async def generate_knockout(
    championship_id: int,
    data: GenerateKnockoutModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    champ_stmt = select(Championship).where(
        Championship.id == championship_id, Championship.owner_id == str(user.id)
    )
    champ = (await session.execute(champ_stmt)).scalar_one_or_none()
    if not champ:
        raise HTTPException(status_code=404, detail="Championship not found.")

    # Check group exists
    group_stmt = select(Group).where(Group.id == data.group_id, Group.championship_id == championship_id)
    group = (await session.execute(group_stmt)).scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")

    return_object = {"round": data.previous_round, "generated": False}

    if data.previous_round == 1:
        return return_object

    group_table = await _get_group_table(session, data.group_id)
    num_participants = len(group_table)
    n_games = (num_participants * (num_participants - 1)) / 2

    if data.previous_round == n_games:
        num_qualified_players, num_knockout_matches = get_knockout_info(num_participants)
    else:
        # Get matches from previous round
        round_matches_stmt = (
            select(Match)
            .where(Match.group_id == data.group_id, Match.round == data.previous_round)
        )
        round_matches = (await session.execute(round_matches_stmt)).scalars().all()

        num_knockout_matches = len(round_matches) // 2
        num_qualified_players = num_knockout_matches * 2

        # Filter by winners
        winners_ids = []
        for m in round_matches:
            if m.goals_1 is not None and m.goals_2 is not None:
                if m.goals_1 > m.goals_2:
                    winners_ids.append(m.participant_1_id)
                else:
                    winners_ids.append(m.participant_2_id)

        group_table = [p for p in group_table if p.participant_id in winners_ids]

    return_object["round"] = num_knockout_matches

    # Check if round already exists
    existing_round_stmt = select(func.count(Match.id)).where(
        Match.group_id == data.group_id, Match.round == num_knockout_matches
    )
    existing_count = (await session.execute(existing_round_stmt)).scalar()

    # Check if redraw needed
    redraw_needed = False
    if existing_count > 0:
        # Check if any match in the previous round was updated after the next round was created
        min_created_stmt = select(func.min(Match.created_at)).where(
            Match.group_id == data.group_id,
            Match.round == num_knockout_matches,
        )
        min_created = (await session.execute(min_created_stmt)).scalar()

        if min_created:
            updated_count_stmt = select(func.count(Match.id)).where(
                Match.group_id == data.group_id,
                Match.round >= num_knockout_matches,
                Match.updated_at > min_created,
            )
            updated_count = (await session.execute(updated_count_stmt)).scalar()
            redraw_needed = updated_count > 0

    if not redraw_needed and existing_count > 0:
        return return_object

    # Delete existing matches from this round and below
    del_stmt = select(Match).where(
        Match.group_id == data.group_id,
        Match.round <= num_knockout_matches,
        Match.round.isnot(None),
    )
    matches_to_delete = (await session.execute(del_stmt)).scalars().all()
    for m in matches_to_delete:
        await session.delete(m)
    await session.flush()

    # Create new knockout matches
    matches_to_create = []
    for i in range(num_knockout_matches):
        if i < len(group_table) and (num_qualified_players - i - 1) < len(group_table):
            p1 = group_table[i].participant_id
            p2 = group_table[num_qualified_players - i - 1].participant_id
            matches_to_create.append(
                Match(
                    group_id=data.group_id,
                    participant_1_id=p1,
                    participant_2_id=p2,
                    round=num_knockout_matches,
                )
            )

    session.add_all(matches_to_create)
    await session.commit()

    return_object["generated"] = True
    return return_object


@router.get("/{championship_id}/group/get", response_model=GroupResponse)
async def get_group(
    championship_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Group).where(Group.championship_id == championship_id).limit(1)
    group = (await session.execute(stmt)).scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")

    return GroupResponse(id=group.id, name=group.name)


@router.get("/{championship_id}/group/matches/{group_id}", response_model=t.List[MatchResponse])
async def list_group_matches(
    championship_id: int,
    group_id: int,
    round: t.Optional[int] = Query(None, description="Round"),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    # Verify group belongs to championship
    group_stmt = select(Group).where(Group.id == group_id, Group.championship_id == championship_id)
    group = (await session.execute(group_stmt)).scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")

    stmt = (
        select(Match)
        .options(
            selectinload(Match.participant_1).selectinload(Participant.team),
            selectinload(Match.participant_2).selectinload(Participant.team),
        )
        .where(Match.group_id == group_id)
    )
    if round is not None:
        stmt = stmt.where(Match.round == round)

    result = await session.execute(stmt)
    matches = result.scalars().all()

    return [_match_to_response(m) for m in matches]


@router.get("/{championship_id}/group/table/{group_id}", response_model=t.List[GroupTableParticipantResponse])
async def get_table(
    championship_id: int,
    group_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    group_stmt = select(Group).where(Group.id == group_id, Group.championship_id == championship_id)
    group = (await session.execute(group_stmt)).scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")

    return await _get_group_table(session, group_id)


@router.delete("/{championship_id}/group/delete/{group_id}")
async def delete_group(
    championship_id: int,
    group_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    group_stmt = select(Group).where(Group.id == group_id, Group.championship_id == championship_id)
    group = (await session.execute(group_stmt)).scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")

    await session.delete(group)
    await session.commit()
    return {"detail": "Group deleted."}
