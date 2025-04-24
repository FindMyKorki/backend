from fastapi import APIRouter, Depends
from users.auth import authenticate_user

from .dataclasses import CreateUserReportRequest
from .service import UserReportsService

user_reports_router = APIRouter()
user_reports_service = UserReportsService()


@user_reports_router.post("/user_reports/{user_id}", response_model=str)
async def create_user_report(
        user_id: str,
        report: CreateUserReportRequest,
        user_response=Depends(authenticate_user)
):
    """Create a new user report for a specific user"""
    return await user_reports_service.create_user_report(user_id, report, user_response.user.id)
