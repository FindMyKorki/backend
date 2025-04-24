from pydantic import BaseModel


class CreateLevelRequest(BaseModel):
    level: str

    class Config:
        from_attributes = True


class Level(CreateLevelRequest):
    id: int

    class Config:
        from_attributes = True
