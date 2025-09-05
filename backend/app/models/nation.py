from pydantic import BaseModel


class nation(BaseModel):
    name: str
    image_path: str
