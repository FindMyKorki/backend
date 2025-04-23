from datetime import datetime
from profiles.dataclasses import Profile
from pydantic import BaseModel
from typing import Optional


class CreateUserReport(BaseModel):
    reason: str
    message: str

    class Config:
        from_attributes = True


class BaseUserReport(BaseModel):
    reason: str
    message: Optional[str]

    class Config:
        from_attributes = True


class UserReport(BaseUserReport):
    id: int
    reported_user: Profile


class CreateUserReport2(BaseUserReport):
    reported_user_id: str


class UpdateUserReport(CreateUserReport):
    id: int
