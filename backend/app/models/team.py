from pydantic import BaseModel


class team(BaseModel):
    id: int
    name: str
    league_name: str
    league_image_path: str
    image_path: str
    participant_id: int
