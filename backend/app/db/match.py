import typing as t

from app.models.match import create_match_model, match, update_match_model
from app.queries.match import (create_matches_query,
                               delete_matches_from_round_and_above_query,
                               get_matches_query, match_exists_query,
                               update_match_query)
from database.db import Database

database = Database()


def list_matches_by_group_and_round(group_id: int, round: int = None) -> t.List[match]:
    query = get_matches_query + f" WHERE m.group_id = {group_id} AND m.round = {round}"
    results = database.execute_select_query(query)

    matches = [match(**r) for r in results]

    return matches


def get_match_by_id(match_id: int) -> match:
    query = get_matches_query + f" WHERE m.id = {match_id} LIMIT 1"
    results = database.execute_select_query(query)
    if not results:
        return None

    return match(**results[0])


def create_matches(data: t.List[create_match_model]) -> None:
    matches_values = []
    for m in data:
        match_str = "("

        match_dict = m.dict()
        match_str = ", ".join(match_dict.values())

        match_str += ")"

        matches_values.append(match_str)

    args = {"matches": ", ".join(matches_values)}
    database.execute_query(create_matches_query, args)


def update_match(data: update_match_model) -> None:
    args = {
        "id": data.match_id,
        "goals_1": data.goals_1,
        "goals_2": data.goals_2,
        "penalties": data.penalties,
    }
    database.execute_query(update_match_query, args)


def check_match_exists(match_id: int) -> bool:
    args = {"match_id": match_id}
    results = database.execute_select_query(match_exists_query, args)

    return len(results) > 0 and results[0]["num_matches"] > 0


def delete_matches_by_round_and_above(group_id: int, round: int) -> None:
    args = {"group_id": group_id, "round": round}
    database.execute_query(delete_matches_from_round_and_above_query, args)
