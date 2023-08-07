from pydantic import BaseModel

class participant(BaseModel):
    id: int
    name: str
    budget: int
    team_name: str
    team_image_path: str