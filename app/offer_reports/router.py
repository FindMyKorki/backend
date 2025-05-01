from fastapi import APIRouter, Depends, Path
from gotrue.types import UserResponse
from users.auth import authenticate_user

from .dataclasses import CreateOfferReport
from .service import OfferReportsService

offer_reports_router = APIRouter()
offer_reports_service = OfferReportsService()


@offer_reports_router.post("/offer_reports/{offer_id}", response_model=str)
async def create_offer_report(
        report: CreateOfferReport,
        offer_id: int = Path(...),
        _user_response: UserResponse = Depends(authenticate_user)
):
    """
    Create a new report for a specific offer.
    
    Args:
        report (CreateOfferReport): The details of the report.
        offer_id (int): The unique identifier of the offer being reported.
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        str: A confirmation message indicating that the offer report has been submitted.
    """
    return await offer_reports_service.create_offer_report(offer_id, report, _user_response.user.id)
