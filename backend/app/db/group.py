import typing as t

from app.queries.group import (
    group_exists_query,
    create_group_query,
    get_group_table_query,
    get_group_query
)
from app.models.group import group_table_participant, group
from database.db import Database

database = Database()


def check_group_exists(group_id: int) -> bool:
    args = {"group_id": group_id}
    results = database.execute_select_query(group_exists_query, args)

    return len(results) > 0 and results[0]["num_groups"] > 0


def create_group(group_name: str) -> int:
    args = {"group_name": group_name}
    group_id = database.execute_query(create_group_query, args)

    return group_id


def get_group() -> group:
    group_instance = database.execute_query(get_group_query)

    return group_instance


def get_group_table(group_id: int) -> t.List[group_table_participant]:
    args = {"group_id": group_id}
    results = database.execute_select_query(get_group_table_query, args)

    if not results:
        return []
    
    group_table = [group_table_participant(**r) for r in results]

    return group_table
