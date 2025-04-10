from fastapi import APIRouter, Path
from datetime import datetime, timezone
from typing import Optional

from .service import TutorsAvailabilityService
from .dataclasses import TutorAvailabilityResponse, TutorAvailabilityRequest, get_end_of_current_month


tutors_availability_router = APIRouter()
tutors_availability_service = TutorsAvailabilityService()


@tutors_availability_router.get("/tutors/{tutor_id}/available-hours", response_model=TutorAvailabilityResponse)
async def get_tutor_available_hours(
    tutor_id: str = Path(...),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    start_date = start_date or datetime.now(timezone.utc)
    end_date = end_date or get_end_of_current_month()
    return await tutors_availability_service.get_tutor_available_hours(tutor_id, start_date, end_date)


@tutors_availability_router.post("/tutors/{tutor_id}/available-hours", response_model=TutorAvailabilityResponse)
async def get_tutor_available_hours_post(
    tutor_id: str = Path(...),
    request: TutorAvailabilityRequest = None
):
    request = request or TutorAvailabilityRequest()
    return await tutors_availability_service.get_tutor_available_hours(tutor_id, request.start_date, request.end_date)