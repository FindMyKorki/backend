from fastapi import APIRouter, Path
from datetime import datetime, timedelta
from typing import Optional

from .service import TutorsAvailabilityService
from .dataclasses import TutorAvailabilityResponse, TutorAvailabilityRequest
from .utils import standardize_datetime


tutors_availability_router = APIRouter()
tutors_availability_service = TutorsAvailabilityService()


@tutors_availability_router.get("/tutors/{tutor_id}/available-hours", response_model=TutorAvailabilityResponse)
async def get_tutor_available_hours(
    tutor_id: str = Path(..., description="Tutor's identifier"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Retrieves available time blocks for a tutor within a specified date range.
    
    Parameters:
    - tutor_id: tutor's identifier
    - start_date: start date of the range (UTC time, optional, default: current time)
    - end_date: end date of the range (UTC time, optional, default: end of current month)
    
    Returns:
    - List of available time blocks for the tutor
    
    Note: It's recommended to include the 'Z' suffix in datetime parameters to explicitly specify UTC timezone.
    """
    request = TutorAvailabilityRequest(
        start_date=start_date,
        end_date=end_date
    )
    
    return await tutors_availability_service.get_tutor_available_hours(tutor_id, request.start_date, request.end_date)


@tutors_availability_router.post("/tutors/{tutor_id}/available-hours", response_model=TutorAvailabilityResponse)
async def get_tutor_available_hours_post(
    tutor_id: str = Path(..., description="Tutor's identifier"),
    request: TutorAvailabilityRequest = None
):
    """
    Retrieves available time blocks for a tutor within a specified date range.
    Request parameters can be provided in the request body.
    
    Parameters:
    - tutor_id: tutor's identifier (path parameter)
    - request: request body containing start_date and end_date
      - start_date: start date of the range (UTC time, optional, default: current time)
      - end_date: end date of the range (UTC time, optional, default: end of current month)
    
    Returns:
    - List of available time blocks for the tutor
    
    Note: It's recommended to include the 'Z' suffix in datetime parameters to explicitly specify UTC timezone.
    """
    if request is None:
        request = TutorAvailabilityRequest()
    
    return await tutors_availability_service.get_tutor_available_hours(tutor_id, request.start_date, request.end_date)
