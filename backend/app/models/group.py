import typing as t

from pydantic import BaseModel

from app.models.match import match
from app.models.participant import participant


class group(BaseModel):
    id: int
    name: str


class create_group_model(BaseModel):
    name: str
    participants: t.List[int]


class generate_knockout_model(BaseModel):
    group_id: int
    previous_round: t.Optional[int] = None


class group_table_participant(BaseModel):
    group_id: int
    participant_id: int
    goals_scored: int
    goals_conceded: int
    wins: int
    losses: int
    draws: int
    goal_difference: int
    points: int
