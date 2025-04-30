from fastapi import APIRouter, Depends
from gotrue.types import UserResponse
from users.auth import authenticate_user

from .dataclasses import CreateIssueReportRequest
from .service import IssueReportsService

issue_reports_router = APIRouter()
issue_reports_service = IssueReportsService()


@issue_reports_router.post("/issue_reports", response_model=str)
async def create_issue_report(report: CreateIssueReportRequest,
                              _user_response: UserResponse = Depends(authenticate_user)
                              ):
    """
    Create a new issue report related to the platform or a specific interaction.

    Args:
        report (CreateIssueReportRequest): The details of the issue being reported (type, description, etc.).
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        str: A confirmation message indicating that the issue report has been submitted.
    """
    return await issue_reports_service.create_issue_report(report, _user_response.user.id)
