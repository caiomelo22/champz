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
    previous_round: int


class group_table_participant(BaseModel):
    group_id: int
    participant_id: int
    name: str
    team_image_path: str
    GF: t.Optional[int]
    GA: t.Optional[int]
    GD: t.Optional[int]
    W: t.Optional[int]
    L: t.Optional[int]
    D: t.Optional[int]
    P: t.Optional[int]
