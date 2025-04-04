from pydantic import BaseModel

class Level(BaseModel):
    id: int
    level: str

    class Config:
        from_attributes = True

class CreateLevelRequest(BaseModel):
    level: str

    class Config:
        from_attributes = True