from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel


class match(BaseModel):
    id: int
    participant_1_id: int
    participant_2_id: int
    participant_1_name: str
    participant_1_team_name: str
    participant_1_team_image_path: str
    participant_2_name: str
    participant_2_team_name: str
    participant_2_team_image_path: str
    goals_1: Optional[int]
    goals_2: Optional[int]
    round: int
    penalties: Optional[bool] = False


class create_match_model(BaseModel):
    group_id: int
    participant_1_id: int
    participant_2_id: int
    round: int


class update_match_model(BaseModel):
    goals_1: int
    goals_2: int
    penalties: Optional[bool] = False
