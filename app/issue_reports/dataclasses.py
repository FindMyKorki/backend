from pydantic import BaseModel


class BaseIssueReport(BaseModel):
    reason: str
    message: str

    class Config:
        from_attributes = True


class IssueReport(BaseIssueReport):
    id: int
