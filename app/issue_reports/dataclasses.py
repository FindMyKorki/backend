from pydantic import BaseModel


class IssueReport(BaseModel):
    id: int
    reason: str
    message: str

    class Config:
        from_attributes = True


class CreateIssueReportRequest(BaseModel):
    reason: str
    message: str

    class Config:
        from_attributes = True


class UpdateIssueReportRequest(BaseModel):
    id: int
    reason: str
    message: str

    class Config:
        from_attributes = True
