import typing as t
from datetime import datetime

from pydantic import BaseModel


class CreateChampionshipModel(BaseModel):
    name: str
    budget_default: int = 250
    player_ids: t.List[str] = []


class UpdateChampionshipModel(BaseModel):
    name: t.Optional[str] = None
    status: t.Optional[str] = None


class ChampionshipResponse(BaseModel):
    id: int
    name: str
    status: str
    budget_default: int
    created_at: datetime
    updated_at: datetime
    num_participants: int = 0
    access_role: str = "owner"
    participant_id: t.Optional[int] = None

    class Config:
        from_attributes = True
