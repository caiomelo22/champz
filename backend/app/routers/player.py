# routes/users.py
import typing as t

from fastapi import APIRouter, HTTPException, Query

from app.db.participant import get_participants_num, update_participant_budget
from app.db.players import buy_player, get_players
from app.db.team import get_participant_by_team
from app.models.player import buy_player_model, player

router = APIRouter()


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
            limit_clause = f"LIMIT {participants_number * 3}"
    if team_participant:
        where_clauses.append(f"team_participant_id = {team_participant}")
    return get_players(where_clauses, limit_clause)


@router.post("/buy/{player_id}")
def buy(
    player_id: str,
    data: buy_player_model,
) -> t.List[player]:
    player_where_clauses = [f"id = '{player_id}'"]
    limit_clause = "LIMIT 1"
    player_results = get_players(player_where_clauses, limit_clause)
    if not player_results:
        raise HTTPException(status_code=400, detail="Invalid player id")

    player_obj = player_results[0]
    if player_obj.team_participant_id:
        # Update original participant budget and reset player's purchase info
        update_participant_budget(player_obj.participant_id, player_obj.value)
        buy_player(player_id)

    if not data.team_participant:
        return True

    participant_id = get_participant_by_team(data.team_participant)
    update_participant_budget(participant_id, data.value)
    buy_player(player_id, data.team_participant, data.value)
