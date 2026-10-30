import typing as t

from pydantic import BaseModel, Field


class ManageParticipantModel(BaseModel):
    team: str
    name: str
    budget: int = Field(ge=0)
    user_email: t.Optional[str] = None


class ParticipantResponse(BaseModel):
    id: int
    name: str
    budget: t.Optional[int] = None
    team_name: t.Optional[str] = None
    team_image_path: t.Optional[str] = None
    user_email: t.Optional[str] = None
    link_status: str = "unlinked"

    class Config:
        from_attributes = True
