# db/crud.py
import typing as t

from fastapi import HTTPException

from app.models.team import team
from app.queries.teams import (add_participant_to_team_query,
                               get_participant_id_by_team_query,
                               get_teams_by_league_query)
from database.db import Database

database = Database()  # Initialize the custom database instance


def add_participant_to_team(participant_id: int, team_id: int) -> None:
    args = {"participant_id": participant_id, "team_id": team_id}
    database.execute_query(add_participant_to_team_query, args)


def get_participant_id_by_team_id(team_id: int) -> int:
    args = {"team_id": team_id}
    results = database.execute_select_query(get_participant_id_by_team_query, args)
    if not results:
        raise HTTPException(status_code=404, detail="Selected team not found")

    return results[0]["participant_id"]


def get_teams_by_league(league_id: int) -> t.List[team]:
    args = {"league_id": league_id}
    results = database.execute_select_query(get_teams_by_league_query, args)

    teams = [team(**r) for r in results]

    return teams
