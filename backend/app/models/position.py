from pydantic import BaseModel


class PositionResponse(BaseModel):
    id: int
    name: str
    specific_positions: str

    class Config:
        from_attributes = True
