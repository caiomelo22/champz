from pydantic import BaseModel

class player(BaseModel):
    id: int
    position: int
    name: str
    nation: int
    league: int
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

