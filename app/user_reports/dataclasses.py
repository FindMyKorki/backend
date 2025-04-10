from pydantic import BaseModel
from typing import Optional
from profiles.dataclasses import Profile


class BaseUserReport(BaseModel):
    reason: str
    message: Optional[str]

    class Config:
        from_attributes = True


class UserReport(BaseUserReport):
    id: int
    reported_user: Profile


class CreateUserReport(BaseUserReport):
    reported_user_id: str


class UpdateUserReport(CreateUserReport):
    id: int
