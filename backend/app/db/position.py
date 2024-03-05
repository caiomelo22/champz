import typing as t

from app.models.position import position
from app.queries.position import list_positions_query
from database.db import Database

database = Database()


def list_positions(where_clause: t.Optional[str] = None) -> t.List[position]:
    query = list_positions_query

    if where_clause:
        query += where_clause

    return database.execute_select_query(query)
