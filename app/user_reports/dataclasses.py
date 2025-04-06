from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserReport(BaseModel):
    id: int
    created_at: datetime
    user_id: str
    reported_user_id: str
    reason: str
    message: str

    class Config:
        from_attributes = True


class CreateUserReport(BaseModel):
    reason: str
    message: str

    class Config:
        from_attributes = True