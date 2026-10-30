from pydantic import BaseModel


class TeamResponse(BaseModel):
    name: str
    image_path: str

    class Config:
        from_attributes = True
