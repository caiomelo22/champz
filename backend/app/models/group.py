import typing as t
from pydantic import BaseModel
from app.models.match import match
from app.models.participant import participant

class group(BaseModel):
    id: int
    name: str
    previous_stage: t.Optional[int] = None
    participants: t.List[participant]
    matches: t.List[match]
