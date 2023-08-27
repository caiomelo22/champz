from app.queries.group import group_exists_query
from database.db import Database

database = Database()


def check_group_exists(group_id: int) -> bool:
    args = {"group_id": group_id}
    results = database.execute_select_query(group_exists_query, args)

    return len(results) > 0 and results[0]["num_groups"] > 0
