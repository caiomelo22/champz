import typing as t

from fastapi import APIRouter, HTTPException

from app.db.group import check_group_exists
from app.db.match import (check_match_exists, create_match, get_match_by_id,
                          list_matches_by_group)
from app.db.participant import get_participants_num
from app.models.match import create_match_model, match, update_match_model

router = APIRouter()


@router.get("/group/{group_id}/list")
def list(group_id: int) -> t.List[match]:
    group_exists = check_group_exists(group_id)
    if not group_exists:
        raise HTTPException(status_code=404, detail="Group not found.")

    return list_matches_by_group(group_id)


def validate_participant(participant_id: int, participant_num: str) -> None:
    participant_exists = get_participants_num(participant_id)
    if not participant_exists:
        raise HTTPException(
            status_code=404, detail=f"Participant {participant_num} not found."
        )


@router.post("/create")
def create(data: create_match_model) -> match:
    group_exists = check_group_exists(data.group_id)
    if not group_exists:
        raise HTTPException(status_code=404, detail="Group not found.")

    validate_participant(data.participant_1_id, "1")
    validate_participant(data.participant_2_id, "2")

    match_id = create_match(data)

    return get_match_by_id(match_id)


@router.post("/update")
def create(data: update_match_model) -> None:
    match_exists = check_match_exists(data.match_id)
    if not match_exists:
        raise HTTPException(status_code=404, detail="Match not found.")

    update_match_model(data)
