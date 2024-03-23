import math
import typing as t
from random import shuffle

from fastapi import APIRouter, HTTPException, Query

from app.db.group import (add_participant_to_group, check_group_exists,
                          create_group, delete_group, get_group,
                          get_group_table)
from app.db.match import (check_redraw_needed, check_round_exists,
                          create_matches, delete_matches_by_round_and_above,
                          list_matches_by_group_and_round)
from app.db.participant import get_participants_ids
from app.models.group import (create_group_model, generate_knockout_model,
                              group, group_table_participant)
from app.models.match import create_match_model, match
from app.utils.helper import get_knockout_info, get_round_winners

router = APIRouter()


@router.post("/create")
def create() -> int:
    participants_list = get_participants_ids()

    group_name = f"G{len(participants_list)}"
    group_id = create_group(group_name)

    for p in participants_list:
        add_participant_to_group(group_id=group_id, participant_id=p)

    matches = []

    # Build the group matches based on the shuffled participants list
    num_participants = len(participants_list)
    n_games = (num_participants * (num_participants - 1)) / 2

    for i in range(num_participants):
        for j in range(i + 1, num_participants):
            matches.append(
                create_match_model(
                    group_id=group_id,
                    participant_1_id=participants_list[i],
                    participant_2_id=participants_list[j],
                    round=n_games,
                )
            )

    shuffle(matches)
    create_matches(matches)

    return group_id


@router.post("/generate-knockout")
def create(data: generate_knockout_model) -> dict:
    # Returns True if a new knockout round is generated ou redrawn
    group_exists = check_group_exists(data.group_id)
    if not group_exists:
        raise HTTPException(status_code=404, detail="Group not found.")

    round_exists = check_round_exists(data.group_id, data.previous_round)
    if not round_exists:
        raise HTTPException(status_code=404, detail="Round not found.")

    return_object = {"round": data.previous_round, "generated": False}

    if data.previous_round == 1:
        return return_object

    group_table = get_group_table(data.group_id)
    num_participants = len(group_table)
    n_games = (num_participants * (num_participants - 1)) / 2

    if data.previous_round == n_games:
        num_qualified_players, num_knockout_matches = get_knockout_info(n_games)
    else:
        round_matches = list_matches_by_group_and_round(
            group_id=data.group_id, round=data.previous_round
        )

        num_knockout_matches = data.previous_round // 2
        num_qualified_players = num_knockout_matches * 2

        # Filter table by only the winner of the current round
        winners_ids = get_round_winners(round_matches)
        group_table = [p for p in group_table if p.participant_id in winners_ids]

    return_object["round"] = num_knockout_matches

    new_round_exists = check_round_exists(data.group_id, num_knockout_matches)
    redraw_needed = check_redraw_needed(data.group_id, data.previous_round)
    if not redraw_needed and new_round_exists:
        return return_object

    # Delete legacy matches from current round and beyond
    delete_matches_by_round_and_above(
        group_id=data.group_id, round=num_knockout_matches
    )

    # Create matches that puts the best participants against the worst qualified
    matches_to_create = []
    for i in range(num_knockout_matches):
        participant_1 = group_table[i].participant_id
        participant_2 = group_table[num_qualified_players - i - 1].participant_id
        match_instance = create_match_model(
            group_id=data.group_id,
            participant_1_id=participant_1,
            participant_2_id=participant_2,
            round=num_knockout_matches,
        )
        matches_to_create.append(match_instance)

        if num_knockout_matches == 2:
            match_instance = create_match_model(
                group_id=data.group_id,
                participant_1_id=participant_1,
                participant_2_id=participant_2,
                round=num_knockout_matches,
            )
            matches_to_create.append(match_instance)


    create_matches(matches_to_create)

    return_object["generated"] = True
    return return_object


@router.get("/get")
def create() -> group:
    group_instance = get_group()
    if not group_instance:
        raise HTTPException(status_code=404, detail="Group not found.")

    return group_instance


@router.get("/matches/{group_id}")
def list_groups(
    group_id: int, round: int = Query(None, description="Round")
) -> t.List[match]:
    group_exists = check_group_exists(group_id)
    if not group_exists:
        raise HTTPException(status_code=404, detail="Group not found.")

    return list_matches_by_group_and_round(group_id, round)


@router.get("/table/{group_id}")
def get_table(group_id: int) -> t.List[group_table_participant]:
    group_exists = check_group_exists(group_id=group_id)
    if not group_exists:
        raise HTTPException(status_code=404, detail="Group not found")

    group_table = get_group_table(group_id)

    return group_table


@router.delete("/delete/{group_id}")
def create(group_id: int) -> None:
    group_exists = check_group_exists(group_id)
    if not group_exists:
        raise HTTPException(status_code=404, detail="Group not found.")

    delete_group(group_id=group_id)
