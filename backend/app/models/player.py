import typing as t

from pydantic import BaseModel


class player(BaseModel):
    id: str
    position_id: int
    position_name: str
    team_participant: t.Optional[str] = None
    team_participant_name: t.Optional[str] = None
    team_participant_image_path: t.Optional[str] = None
    participant_id: t.Optional[int] = None
    team_origin: str
    team_origin_name: str
    team_origin_image_path: str
    name: str
    nation: str
    nation_name: str
    nation_image_path: str
    specific_position: str
    overall: int
    pace: int
    shooting: int
    passing: int
    dribbling: int
    defending: int
    physical: int
    image_path: str
    value: t.Optional[int] = None


class buy_player_model(BaseModel):
    team_participant: t.Optional[str] = None
    value: t.Optional[int] = None
