# db/crud.py
import typing as t

from fastapi import HTTPException

from app.models.team import team
from app.queries.teams import (
    add_participant_to_team_query,
    get_participant_id_by_team_query,
    get_most_popular_teams_query,
)
from database.db import Database

database = Database()  # Initialize the custom database instance


def add_participant_to_team(participant_id: int, team_name: str) -> None:
    args = (
        participant_id,
        team_name,
    )
    database.execute_query(add_participant_to_team_query, args)


def get_participant_id_by_team_name(team_name: str) -> int:
    args = (team_name,)
    results = database.execute_select_query(get_participant_id_by_team_query, args)
    if not results:
        raise HTTPException(status_code=404, detail="Selected team not found")

    return results[0]["participant_id"]


def get_most_popular_teams() -> t.List[team]:
    results = database.execute_select_query(get_most_popular_teams_query)

    teams = [team(**r) for r in results]

    return teams
