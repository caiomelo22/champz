# db/crud.py

import typing as t
from app.models.player import player
from app.queries.players import players_query
from database.db import Database

database = Database()  # Initialize the custom database instance

# CRUD operations for items
def get_players() -> t.List[player]:
    results = database.execute_select_query(players_query)
    players = [player(**r) for r in results]

    return players





