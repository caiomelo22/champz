from pydantic import BaseModel

class position(BaseModel):
    id: int
    name: str
    specific_positions: str

