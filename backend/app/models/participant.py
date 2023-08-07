from pydantic import BaseModel

class participant(BaseModel):
    id: int
    name: str
    budget: int