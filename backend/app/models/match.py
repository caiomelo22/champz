import typing as t

from pydantic import BaseModel


class MatchResponse(BaseModel):
    id: int
    participant_1_id: int
    participant_2_id: int
    participant_1_name: str
    participant_1_team_name: str
    participant_1_team_image_path: str
    participant_2_name: str
    participant_2_team_name: str
    participant_2_team_image_path: str
    goals_1: t.Optional[int] = None
    goals_2: t.Optional[int] = None
    round: t.Optional[int] = None
    penalties: t.Optional[bool] = False

    class Config:
        from_attributes = True


class UpdateMatchModel(BaseModel):
    goals_1: int
    goals_2: int
    penalties: t.Optional[bool] = False
