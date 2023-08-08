from pydantic import BaseModel


class league(BaseModel):
    id: int
    name: str
    image_path: str
