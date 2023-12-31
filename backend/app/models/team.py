import typing as t

from pydantic import BaseModel


class team(BaseModel):
    id: int
    name: str
    image_path: str
    participant_id: t.Optional[int]
