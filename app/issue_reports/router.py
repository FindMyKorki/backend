from fastapi import APIRouter, Depends
from users.auth import authenticate_user

from .dataclasses import CreateIssueReport
from .service import IssueReportsService

issue_reports_router = APIRouter()
issue_reports_service = IssueReportsService()


@issue_reports_router.post("/issue_reports", response_model=str)
async def create_issue_report(report: CreateIssueReport, user_response=Depends(authenticate_user)):
    """Create a new issue report"""
    return await issue_reports_service.create_issue_report(report, user_response.user.id)
