import typing as t

from app.models.match import create_match_model, match, update_match_model
from app.queries.match import (create_match_query, get_matches_query,
                               match_exists_query, update_match_query)
from database.db import Database

database = Database()


def list_matches_by_group(group_id: int) -> t.List[match]:
    query = get_matches_query + f" WHERE m.group_id = {group_id}"
    results = database.execute_select_query(query)

    matches = [match(**r) for r in results]

    return matches


def get_match_by_id(match_id: int) -> match:
    query = get_matches_query + f" WHERE m.id = {match_id} LIMIT 1"
    results = database.execute_select_query(query)
    if not results:
        return None

    return match(**results[0])


def create_match(data: create_match_model) -> int:
    args = {
        "group_id": data.group_id,
        "participant_1_id": data.participant_1_id,
        "participant_2_id": data.participant_2_id,
        "round": data.round,
    }
    match_id = database.execute_query(create_match_query, args)
    return match_id


def update_match(data: update_match_model) -> None:
    args = {
        "id": data.match_id,
        "goals_1": data.goals_1,
        "goals_2": data.goals_2,
    }
    database.execute_query(update_match_query, args)


def check_match_exists(match_id: int) -> bool:
    args = {"match_id": match_id}
    results = database.execute_select_query(match_exists_query, args)

    return len(results) > 0 and results[0]["num_matches"] > 0
