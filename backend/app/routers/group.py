import math
import typing as t
from random import shuffle

from fastapi import APIRouter, HTTPException, Query

from app.db.group import (add_participant_to_group, check_group_exists,
                          create_group, delete_group, get_group,
                          get_group_table)
from app.db.match import (create_matches, delete_matches_by_round_and_above,
                          list_matches_by_group_and_round)
from app.models.group import (create_group_model, generate_knockout_model,
                              group, group_table_participant)
from app.models.match import create_match_model, match
from app.utils.helper import get_knockout_info

router = APIRouter()


@router.post("/create")
def create(data: create_group_model) -> int:
    group_id = create_group(data.name)

    participants_list = data.participants

    for p in participants_list:
        add_participant_to_group(group_id=group_id, participant_id=p)

    shuffle(participants_list)

    matches = []

    # Build the group matches based on the shuffled participants list
    half = math.floor(len(participants_list) / 2)
    first_half = participants_list[:half]
    second_half = participants_list[half:]

    for _ in range(len(participants_list)):
        for j in range(len(first_half)):
            matches.append(
                create_match_model(
                    group_id=group_id,
                    participant_1_id=first_half[j],
                    participant_2_id=list(reversed(second_half))[j],
                )
            )
        first_half.append(second_half.pop(0))
        second_half.append(first_half.pop(0))

    create_matches(matches)

    return group_id


@router.post("/generate-knockout")
def create(data: generate_knockout_model) -> None:
    group_exists = check_group_exists(data.group_id)
    if not group_exists:
        raise HTTPException(status_code=404, detail="Group not found.")
    if data.previous_round == 1:
        return

    group_table = get_group_table(data.group_id)

    if not data.previous_round:
        num_qualified_players, num_knockout_matches = get_knockout_info(
            len(group_table)
        )
    else:
        round_matches = list_matches_by_group_and_round(
            group_id=data.group_id, round=data.previous_round
        )

        num_knockout_matches = len(round_matches) // 2
        num_qualified_players = num_knockout_matches * 2

        # Filter table by only the winner of the current round
        winners_ids = [
            m.participant_1_id if m.goals_1 > m.goals_2 else m.participant_2_id
            for m in round_matches
        ]
        group_table = [p for p in group_table if p.participant_id in winners_ids]

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

    create_matches(matches_to_create)


@router.get("/get")
def create() -> group:
    group_instance = get_group()

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
