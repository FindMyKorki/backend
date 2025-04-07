from pydantic import BaseModel
from typing import Optional


class Profile(BaseModel):
    id: str
    full_name: Optional[str]
    is_tutor: bool
    avatar_url: Optional[str]

    class Config:
        from_attributes = True


class UpsertProfile(BaseModel):
    full_name: Optional[str]
    is_tutor: bool
    avatar_url: Optional[str]

    class Config:
        from_attributes = True
