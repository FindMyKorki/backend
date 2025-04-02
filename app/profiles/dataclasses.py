from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Profile(BaseModel):
    id: str
    full_name: Optional[str] = None
    is_tutor: bool
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

class CreateProfile(BaseModel):
    full_name: str
    is_tutor: bool

    class Config:
        from_attributes = True