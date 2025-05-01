from fastapi import APIRouter, Depends, Path
from gotrue.types import UserResponse
from users.auth import authenticate_user

from .dataclasses import CreateUserReportRequest
from .service import UserReportsService

user_reports_router = APIRouter()
user_reports_service = UserReportsService()


@user_reports_router.post("/user_reports/{user_id}", response_model=str)
async def create_user_report(report: CreateUserReportRequest, user_id: str = Path(...),
                             _user_response: UserResponse = Depends(authenticate_user)):
    """
    Create a new user report for a specific user.

    Args:
        user_id (str): The UUID of the user the report is being created for.
        report (CreateUserReportRequest): The data needed to create the user report, such as the report's content and type.
        _user_response (UserResponse): The authenticated user making the request.

    Returns:
        str: A confirmation message or the ID of the newly created user report.
    """
    return await user_reports_service.create_user_report(user_id, report, _user_response.user.id)
