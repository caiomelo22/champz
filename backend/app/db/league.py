from fastapi import HTTPException

from app.queries.league import league_exists_query
from database.db import Database

database = Database()


def check_league_exists(league_id: int) -> bool:
    args = {"league_id": league_id}
    results = database.execute_select_query(league_exists_query, args)

    return not results or not results[0]["num_leagues"]
