from pydantic import BaseModel
from typing import Optional

class UpdateProfileRequest(BaseModel):
    full_name: str
    remove_avatar: Optional[bool] = False

class CreateProfileRequest(BaseModel):
    full_name: str
    is_tutor: bool

class BaseProfile(CreateProfileRequest):
    avatar_url: Optional[str]

    class Config:
        from_attributes = True


class Profile(BaseProfile):
    id: str