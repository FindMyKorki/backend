from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class IssueReport(BaseModel):
    id: int
    created_at: datetime
    user_id: str
    reason: str
    message: str

    class Config:
        from_attributes = True


class CreateIssueReport(BaseModel):
    reason: str
    message: str

    class Config:
        from_attributes = True