from datetime import datetime
from pydantic import BaseModel


class TestLesson(BaseModel):
    id: int
    created_at: datetime
    name: str
    description: str

    class Config:
        from_attributes = True


class CreateTestLesson(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True
