# db/crud.py

from fastapi import HTTPException

from app.queries.participants import (change_participant_budget_query,
                                      get_participant_budget_query,
                                      num_participants_query)
from database.db import Database

database = Database()  # Initialize the custom database instance


def get_participants_num(participant_id: int) -> int:
    query = num_participants_query
    if participant_id:
        query += f" WHERE id = {participant_id}"
    result = database.execute_select_query(query)

    return result[0]["num_participants"]


def get_participant_budget(participant_id: int) -> int:
    args = {"participant_id": participant_id}
    results = database.execute_select_query(get_participant_budget_query, args)
    if not results:
        raise HTTPException(status_code=404, detail="Participant not found")

    return results[0]["budget"]


def update_participant_budget(participant_id: int, value: int) -> None:
    current_budget = get_participant_budget(participant_id)
    if current_budget - value < 0:
        raise HTTPException(
            status_code=400, detail="Participant does not have enough budget"
        )

    args = {"participant_id": participant_id, "value": value}
    database.execute_query(change_participant_budget_query, args)
