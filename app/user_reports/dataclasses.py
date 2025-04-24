from datetime import datetime
from profiles.dataclasses import Profile
from pydantic import BaseModel
from typing import Optional


class CreateUserReportRequest(BaseModel):
    reason: str
    message: Optional[str] = None

    class Config:
        from_attributes = True


class BaseUserReport(BaseModel):
    reason: str
    message: Optional[str]

    class Config:
        from_attributes = True


class UserReport(CreateUserReportRequest):
    id: int
    reported_user: Profile
    created_at: datetime


class CreateUserReport2(BaseUserReport):
    reported_user_id: str


class UpdateUserReport(CreateUserReportRequest):
    id: int
