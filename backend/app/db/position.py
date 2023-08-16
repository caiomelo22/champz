import typing as t

from app.models.position import position
from app.queries.position import list_positions_query
from database.db import Database

database = Database()


def list_positions() -> t.List[position]:
    return database.execute_select_query(list_positions_query)
