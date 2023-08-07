from pydantic import BaseModel

class group_participant(BaseModel):
    id: int
    group_id: int
    participant_id: int
