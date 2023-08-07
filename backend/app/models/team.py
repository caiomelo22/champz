from pydantic import BaseModel

class team(BaseModel):
    id: int
    name: str
    league_id: int
    image_path: str
    participant_id: int

