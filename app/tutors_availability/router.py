from datetime import datetime, timezone
from fastapi import APIRouter, Path
from typing import Optional

from .dataclasses import TutorAvailabilityResponse
from .service import TutorsAvailabilityService
from .utils import get_end_of_month

tutors_availability_router = APIRouter()
tutors_availability_service = TutorsAvailabilityService()


@tutors_availability_router.get("/tutors/{tutor_id}/available-hours", response_model=TutorAvailabilityResponse)
async def get_tutor_available_hours(
        tutor_id: str = Path(...),
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
):
    """
    Retrieve the available hours for a specific tutor within a given date range.

    Args:
        tutor_id (str): The UUID of the tutor whose available hours are being requested.
        start_date (Optional[datetime]): The start date for the availability range. Defaults to the current date and time if not provided.
        end_date (Optional[datetime]): The end date for the availability range. Defaults to the end of start_date month if not provided.

    Returns:
        TutorAvailabilityResponse: A response object containing the tutor's available hours within the specified date range.
    """
    start_date = start_date or datetime.now(timezone.utc)
    end_date = end_date or get_end_of_month(start_date)
    return await tutors_availability_service.get_tutor_available_hours(tutor_id, start_date, end_date)
