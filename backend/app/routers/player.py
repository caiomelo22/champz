# routes/users.py
import typing as t

from fastapi import APIRouter, HTTPException, Query

from app.db.participant import get_participants_num, update_participant_budget
from app.db.players import buy_player, get_player_by_id, get_players
from app.db.team import get_participant_id_by_team_id
from app.models.player import buy_player_model, player

router = APIRouter()

def get_player_limit(participants_number, position):
    position = int(position)
    if not participants_number:
        return 0
    elif position == 1:
        return 5
    elif position == 2:
        return 12
    elif position == 3:
        return 10
    elif position == 4:
        return 8
    elif position == 5:
        return 7
    elif position == 6:
        return 12
    elif position == 7:
        return 8

@router.get("/list")
def list(
    position: str = Query(None, description="Filter by position"),
    team_participant: str = Query(None, description="Filter by team participant"),
) -> t.List[player]:
    where_clauses = []
    limit_clause = ""
    if position:
        where_clauses.append(f"position_id = {position}")
        participants_number = get_participants_num()
        if participants_number:
            limit_clause = f" LIMIT {get_player_limit(participants_number, position)}"
    if team_participant:
        where_clauses.append(f"team_participant_id = {team_participant}")
    return get_players(where_clauses, limit_clause)


@router.post("/buy/{player_id}")
def buy(
    player_id: str,
    data: buy_player_model,
) -> player:
    player_instance = get_player_by_id(player_id)
    if not player_instance:
        raise HTTPException(status_code=404, detail="Player not found.")

    if player_instance.team_participant_id:
        # Update original participant budget and reset player's purchase info
        update_participant_budget(player_instance.participant_id, player_instance.value)
        buy_player(player_id)

    if not data.team_participant:
        return get_player_by_id(player_id)

    if not data.value:
        raise HTTPException(status_code=400, detail="Player value not valid")

    participant_id = get_participant_id_by_team_id(data.team_participant)
    update_participant_budget(participant_id, -data.value)
    buy_player(player_id, data.team_participant, data.value)

    return get_player_by_id(player_id)
