import typing as t

from app.models.group import group, group_table_participant
from app.queries.group import (add_participant_to_group_query,
                               create_group_query, delete_group_query,
                               get_group_query, get_group_table_query,
                               group_exists_query)
from database.db import Database

database = Database()


def add_participant_to_group(group_id: int, participant_id: int) -> None:
    args = (
        group_id,
        participant_id,
    )
    database.execute_query(add_participant_to_group_query, args)


def check_group_exists(group_id: int) -> bool:
    args = (group_id,)
    results = database.execute_select_query(group_exists_query, args)

    return len(results) > 0 and results[0]["num_groups"] > 0


def create_group(group_name: str) -> int:
    args = (group_name,)
    group_id = database.execute_query(create_group_query, args)

    return group_id


def get_group() -> group:
    results = database.execute_select_query(get_group_query)
    if not results:
        return None

    return group(**results[0])


def get_group_table(group_id: int) -> t.List[group_table_participant]:
    args = (group_id,)
    results = database.execute_select_query(get_group_table_query, args)

    if not results:
        return []

    group_table = [group_table_participant(**r) for r in results]

    return group_table


def delete_group(group_id: int) -> None:
    args = (group_id,)
    database.execute_query(delete_group_query, args)
