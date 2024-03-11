# db/crud.py

import typing as t

from app.models.player import player
from app.queries.players import (
    buy_player_query,
    change_players_team_query,
    player_exists_by_id_query,
    players_query,
    reset_players_team_by_participant_id_query,
    player_transfers_query,
)
from database.db import Database

database = Database()  # Initialize the custom database instance


def get_players(where_clauses: t.List[str], limit_clause: str = "") -> t.List[player]:
    where_clause_str = ""
    if where_clauses:
        where_clause_str = " WHERE " + " AND ".join(where_clauses)
    order_by_clause_str = " ORDER BY player.overall DESC, player.pace DESC"
    query = players_query + where_clause_str + order_by_clause_str + limit_clause
    results = database.execute_select_query(query)
    players = [player(**r) for r in results]

    return players


def get_player_by_id(player_id: str) -> player:
    where_clause = f" WHERE player.id = '{player_id}'"
    limit_clause = " LIMIT 1"
    query = players_query + where_clause + limit_clause
    results = database.execute_select_query(query)
    if not results:
        return None

    player_instance = player(**results[0])

    return player_instance


def check_player_exists(player_id: str) -> bool:
    args = {"player_id": player_id}
    result = database.execute_select_query(player_exists_by_id_query, args)

    return result[0]["player_count"] > 0


def buy_player(
    player_id: str,
    team_participant_id: t.Optional[int] = None,
    value: t.Optional[int] = None,
) -> None:
    args = (
        team_participant_id,
        value,
        player_id,
    )
    database.execute_query(buy_player_query, args)


def change_players_team(new_team_id: int, old_team_id: int) -> None:
    args = (
        new_team_id,
        old_team_id,
    )
    database.execute_query(change_players_team_query, args)


def reset_players_team_by_participant_id(participant_id: int) -> None:
    args = (participant_id,)
    database.execute_query(reset_players_team_by_participant_id_query, args)


def get_player_transfers() -> t.Any:
    results = database.execute_select_query(player_transfers_query)

    return results
