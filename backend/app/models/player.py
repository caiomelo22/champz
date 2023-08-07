import typing as t
from pydantic import BaseModel

class player(BaseModel):
    id: str
    position_id: int
    position_name: str
    team_participant_id: t.Optional[int] = None
    team_participant_name: t.Optional[str] = None
    team_participant_image_path: t.Optional[str] = None
    team_origin_id: int
    team_origin_name: str
    team_origin_image_path: str
    name: str
    nation_id: int
    nation_name: str
    nation_image_path: str
    specific_position: str
    skills: str
    weak_foot: str
    work_rate: str
    pace: int
    shooting: int
    passing: int
    dribbling: int
    defending: int
    physical: int
    image_path: str

