from pydantic import BaseModel

class group(BaseModel):
    id: int
    name: str
    previous_stage: int
