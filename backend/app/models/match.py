from pydantic import BaseModel

class match(BaseModel):
    id: int
    group_id: int
    participant_1_id: int
    participant_2_id: int
    goals_1: int
    goals_2: int