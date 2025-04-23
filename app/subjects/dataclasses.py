from pydantic import BaseModel
from typing import Optional


class CreateSubjectRequest(BaseModel):
    name: str
    icon_url: str
    is_custom: bool = False

    class Config:
        from_attributes = True


class Subject(CreateSubjectRequest):
    id: int


class UpsertSubject(CreateSubjectRequest):
    icon_url: Optional[str] = None
