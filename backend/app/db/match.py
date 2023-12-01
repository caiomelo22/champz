import typing as t
from datetime import datetime as dt

from app.models.match import create_match_model, match, update_match_model
from app.queries.match import (create_matches_query,
                               delete_matches_from_round_and_above_query,
                               get_matches_query, match_exists_by_id_query,
                               redraw_needed_query, round_exists_by_id_query,
                               update_match_query)
from database.db import Database

database = Database()


def list_matches_by_group_and_round(group_id: int, round: int = None) -> t.List[match]:
    query = get_matches_query + f" WHERE m.group_id = {group_id}"
    if round:
        query += f" AND m.round = {round}"

    query += " ORDER BY m.id"
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
    for m in data:
        match_dict = m.dict()

        now = dt.now().isoformat()
        match_dict["created_at"] = now
        match_dict["updated_at"] = now

        database.execute_query(create_matches_query, tuple(match_dict.values()))


def update_match(match_id: int, data: update_match_model) -> None:
    updated_at = dt.now().isoformat()
    args = (data.goals_1, data.goals_2, data.penalties, updated_at, match_id)
    database.execute_query(update_match_query, args)


def check_round_exists(group_id: int, round: int) -> bool:
    args = (
        group_id,
        round,
    )
    results = database.execute_select_query(round_exists_by_id_query, args)

    return len(results) > 0 and results[0]["num_matches"] > 0


def check_match_exists(match_id: int) -> bool:
    args = (match_id,)
    results = database.execute_select_query(match_exists_by_id_query, args)

    return len(results) > 0 and results[0]["num_matches"] > 0


def delete_matches_by_round_and_above(group_id: int, round: int) -> None:
    args = (
        group_id,
        round,
    )
    database.execute_query(delete_matches_from_round_and_above_query, args)


def check_redraw_needed(group_id: int, round: int) -> bool:
    args = (
        group_id,
        round,
        group_id,
        round,
    )
    results = database.execute_select_query(redraw_needed_query, args)

    return len(results) > 0 and results[0]["num_matches_updated"] > 0
