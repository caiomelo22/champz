import typing as t

from pydantic import BaseModel


class GroupResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class GenerateKnockoutModel(BaseModel):
    group_id: int
    previous_round: int


class GroupTableParticipantResponse(BaseModel):
    group_id: int
    participant_id: int
    name: str
    team_image_path: t.Optional[str] = None
    GF: int = 0
    GA: int = 0
    GD: int = 0
    W: int = 0
    L: int = 0
    D: int = 0
    P: int = 0

    class Config:
        from_attributes = True
