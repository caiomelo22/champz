from pydantic import BaseModel

class player(BaseModel):
    id: str
    position_id: int
    team_origin_id: int
    team_participant_id: int
    name: str
    nation_id: int
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

