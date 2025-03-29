from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from typing import Optional

from .service import TutorsAvailabilityService
from .dataclasses import TutorAvailabilityResponse
from .utils import standardize_datetime


tutors_availability_router = APIRouter()
tutors_availability_service = TutorsAvailabilityService()


@tutors_availability_router.get("/tutors/{tutor_id}/available-hours", response_model=TutorAvailabilityResponse)
async def get_tutor_available_hours(
    tutor_id: str,
    start_date: datetime = Query(..., description="Start date of the range (UTC, e.g. 2024-01-01T00:00:00Z)"),
    end_date: Optional[datetime] = Query(None, description="End date of the range (UTC, default: +7 days from start date)")
):
    """
    Retrieves available time blocks for a tutor within a specified date range.
    
    Parameters:
    - tutor_id: tutor's identifier
    - start_date: start date of the range (UTC time, format: YYYY-MM-DDTHH:MM:SSZ)
    - end_date: end date of the range (UTC time, optional, default: +7 days from start date)
    
    Returns:
    - List of available time blocks for the tutor
    
    Note: It's recommended to include the 'Z' suffix in datetime parameters to explicitly specify UTC timezone.
    """
    # Ensure dates have timezone information
    start_date = standardize_datetime(start_date)
    
    if end_date is None:
        end_date = start_date + timedelta(days=7)
    else:
        end_date = standardize_datetime(end_date)
    
    return await tutors_availability_service.get_tutor_available_hours(tutor_id, start_date, end_date) 