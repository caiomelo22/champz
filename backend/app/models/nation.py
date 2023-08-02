from pydantic import BaseModel

class nation(BaseModel):
    id: int
    name: str
    image_path: str
