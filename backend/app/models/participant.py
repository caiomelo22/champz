import typing as t

from pydantic import BaseModel


class participant(BaseModel):
    id: int
    name: str
    budget: int
    team_name: str
    team_image_path: str


class manage_participant_model(BaseModel):
    team: str
    name: str
    budget: int
