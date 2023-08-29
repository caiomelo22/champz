from typing import List

from app.models.league import league
from app.queries.league import get_leagues_query, league_exists_query
from database.db import Database

database = Database()


def check_league_exists(league_id: int) -> bool:
    args = (league_id,)
    results = database.execute_select_query(league_exists_query, args)

    return len(results) > 0 and results[0]["num_leagues"] > 0


def get_leagues() -> List[league]:
    results = database.execute_select_query(get_leagues_query)

    leagues = [league(**r) for r in results]

    return leagues
