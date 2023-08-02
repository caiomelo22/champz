from pydantic import BaseModel

class team(BaseModel):
    id: int
    name: str
    league: int
    image_path: str

