# db/crud.py

from app.queries.teams import get_participant_id_by_team_query
from database.db import Database

database = Database()  # Initialize the custom database instance


def get_participant_by_team(team_id: int) -> int:
    args = {"team_id": team_id}
    results = database.execute_select_query(get_participant_id_by_team_query, args)
    if not results:
        return None

    return results[0]["participant_id"]
