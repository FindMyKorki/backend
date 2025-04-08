from fastapi import APIRouter, Depends
from users.auth import authenticate_user
from .service import OfferReportsService
from .dataclasses import CreateOfferReport


offer_reports_router = APIRouter()
offer_reports_service = OfferReportsService()


@offer_reports_router.post("/offer_reports/{offer_id}", response_model=str)
async def create_offer_report(
    offer_id: int, 
    report: CreateOfferReport, 
    user_response=Depends(authenticate_user)
):
    """Create a new report for a specific offer"""
    return await offer_reports_service.create_offer_report(offer_id, report, user_response.user.id)