import typing as t

from fastapi import HTTPException

from app.models.participant import participant
from app.queries.participants import (change_participant_budget_query,
                                      get_participant_budget_query,
                                      insert_participant_query,
                                      list_participants_query,
                                      num_participants_query,
                                      update_participant_query)
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


def get_participants() -> t.List[participant]:
    results = database.execute_select_query(list_participants_query)
    participants = [participant(**r) for r in results]

    return participants


def get_participant_by_id(participant_id: int) -> participant:
    query = list_participants_query + "WHERE p.participant_id = :participant_id LIMIT 1"
    args = {"participant_id": participant_id}
    results = database.execute_select_query(query, args)
    if not results:
        return None

    participant_instance = participant(**results[0])
    return participant_instance


def create_participant(name: str, budget: int) -> None:
    args = {"name": name, "budget": budget}
    participant_id = database.execute_query(insert_participant_query, args)
    return participant_id


def update_participant(name: str, budget: int) -> None:
    args = {"name": name, "budget": budget}
    participant_id = database.execute_query(update_participant_query, args)
    return participant_id
