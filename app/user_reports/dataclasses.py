from pydantic import BaseModel
from typing import Optional
from profiles.dataclasses import Profile


class UserReport(BaseModel):
    id: int
    reported_user: Profile
    reason: str
    message: Optional[str]

    class Config:
        from_attributes = True


class CreateUserReportRequest(BaseModel):
    reported_user_id: str
    reason: str
    message: Optional[str]

    class Config:
        from_attributes = True


class UpdateUserReportRequest(BaseModel):
    id: int
    reported_user_id: str
    reason: str
    message: Optional[str]

    class Config:
        from_attributes = True
