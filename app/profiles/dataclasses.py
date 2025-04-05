from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CreateProfile(BaseModel):
    full_name: str
    is_tutor: bool

    class Config:
        from_attributes = True


class Profile(CreateProfile):
    id: str
    is_tutor: bool
