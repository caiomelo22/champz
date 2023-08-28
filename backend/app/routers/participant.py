import typing as t

from fastapi import APIRouter, HTTPException

from app.db.participant import (create_participant, delete_participant,
                                get_participant_by_id, get_participants,
                                update_participant)
from app.db.players import (change_players_team,
                            reset_players_team_by_participant_id)
from app.db.team import add_participant_to_team, get_participant_id_by_team_id
from app.models.participant import manage_participant_model, participant

router = APIRouter()


@router.get("/list")
def list() -> t.List[participant]:
    return get_participants()


@router.post("/create")
def create(data: manage_participant_model) -> participant:
    existing_participant_id = get_participant_id_by_team_id(data.team)
    if existing_participant_id:
        raise HTTPException(
            status_code=400,
            detail="The chosen team has already been assigned to another participant.",
        )
    participant_id = create_participant(data.name, data.budget)
    add_participant_to_team(participant_id, data.team)
    return get_participant_by_id(participant_id)


@router.patch("/update/{participant_id}")
def create(participant_id: int, data: manage_participant_model) -> participant:
    participant_instance = get_participant_by_id(participant_id)
    if not participant_instance:
        raise HTTPException(
            status_code=404,
            detail="Participant not found.",
        )

    new_team_participant_id = get_participant_id_by_team_id(data.team)
    if new_team_participant_id and new_team_participant_id != participant_id:
        raise HTTPException(
            status_code=400,
            detail="The chosen team has already been assigned to another participant.",
        )
    elif data.team != participant_instance.team_id:
        change_players_team(
            new_team_id=data.team, old_team_id=participant_instance.team_id
        )

        # Reseting participant's old team
        add_participant_to_team(None, participant_instance.team_id)

        # Adding participant to new team
        add_participant_to_team(participant_id, data.team)

    # Updating name and budget fields
    update_participant(data.name, data.budget, participant_id)

    return get_participant_by_id(participant_id)


@router.delete("/delete/{participant_id}")
def delete(participant_id: int) -> None:
    participant_instance = get_participant_by_id(participant_id)
    if not participant_instance:
        raise HTTPException(
            status_code=404,
            detail="Participant not found.",
        )

    reset_players_team_by_participant_id(participant_id)
    delete_participant(participant_id)
