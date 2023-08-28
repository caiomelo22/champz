import typing as t

from fastapi import HTTPException

from app.models.participant import participant
from app.queries.participants import (change_participant_budget_query,
                                      delete_participant_query,
                                      get_participant_budget_query,
                                      insert_participant_query,
                                      list_participants_query,
                                      num_participants_query,
                                      update_participant_query)
from database.db import Database

database = Database()  # Initialize the custom database instance


def get_participants_num(participant_id: int = None) -> int:
    query = num_participants_query
    if participant_id:
        query += f" WHERE id = {participant_id}"
    result = database.execute_select_query(query)

    return result[0]["num_participants"]


def get_participant_budget(participant_id: int) -> int:
    args = (participant_id,)
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

    args = (
        value,
        participant_id,
    )
    database.execute_query(change_participant_budget_query, args)


def get_participants() -> t.List[participant]:
    results = database.execute_select_query(list_participants_query)
    participants = [participant(**r) for r in results]

    return participants


def get_participant_by_id(participant_id: int) -> participant:
    query = list_participants_query + f" WHERE p.id = {participant_id} LIMIT 1"
    results = database.execute_select_query(query)
    if not results:
        return None

    participant_instance = participant(**results[0])
    return participant_instance


def create_participant(name: str, budget: int) -> None:
    args = (
        name,
        budget,
    )
    participant_id = database.execute_query(insert_participant_query, args)
    return participant_id


def update_participant(name: str, budget: int, participant_id: int) -> None:
    args = (
        name,
        budget,
        participant_id,
    )
    database.execute_query(update_participant_query, args)


def delete_participant(participant_id: int) -> None:
    args = (participant_id,)
    database.execute_query(delete_participant_query, args)
