from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class CreateIssueReportRequest(BaseModel):
    reason: str
    message: str

    class Config:
        from_attributes = True

class IssueReport(CreateIssueReportRequest):
    id: int
    created_at: datetime
    user_id: str

    class Config:
        from_attributes = True
