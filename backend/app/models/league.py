from pydantic import BaseModel

class league(BaseModel):
    id: int
    name: str
    nation: int
    image_path: str

