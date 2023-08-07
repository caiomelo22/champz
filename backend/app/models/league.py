from pydantic import BaseModel

class league(BaseModel):
    id: int
    name: str
    nation_id: int
    image_path: str

