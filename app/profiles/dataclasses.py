from pydantic import BaseModel
from typing import Optional


class BaseProfile(BaseModel):
    full_name: str
    is_tutor: bool
    avatar_url: Optional[str]

    class Config:
        from_attributes = True


class Profile(BaseProfile):
    id: str
