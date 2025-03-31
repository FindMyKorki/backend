from datetime import datetime
from pydantic import BaseModel


class Profile(BaseModel):
    id: str
    full_name: str
    is_tutor: bool
    avatar_url: str

    class Config:
        from_attributes = True

class CreateProfile(BaseModel):
    full_name: str
    is_tutor: bool

    class Config:
        from_attributes = True