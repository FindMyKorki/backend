from pydantic import BaseModel
from typing import Optional

class UpdateProfileRequest(BaseModel):
    full_name: str
    remove_avatar: Optional[bool] = False

class SetRoleRequest(BaseModel):
    is_tutor: bool

    class Config:
        from_attributes = True

class CreateProfileRequest(SetRoleRequest):
    full_name: str

class BaseProfile(CreateProfileRequest):
    avatar_url: Optional[str] = None
    id: str

    class Config:
        from_attributes = True


class Profile(BaseModel):
    id: str
    is_tutor: bool

    class Config:
        from_attributes = True