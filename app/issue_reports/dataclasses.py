from datetime import datetime
from pydantic import BaseModel
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


class BaseIssueReport(BaseModel):
    reason: str
    message: str

    class Config:
        from_attributes = True


class IssueReport2(BaseIssueReport):
    id: int
