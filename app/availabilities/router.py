from fastapi import APIRouter, Depends, Path, Query
from gotrue.types import UserResponse
from users.auth import authenticate_user

from .dataclasses import AvailabilityHours, UnavailabilityHours
from .service import AvailabilityService

availabilities_router = APIRouter()
availabilities_service = AvailabilityService()


@availabilities_router.get("/availabilities/{tutor_id}", response_model=list[AvailabilityHours])
async def get_tutor_availabilities(tutor_id: str = Path(...)) -> list[AvailabilityHours]:
    """
    Get a list of availability slots for a specific tutor

    Args:
        tutor_id (str): Tutor UUID

    Returns:
        List[AvailabilityHours]: A list of time slots when the tutor is available
    """
    return await availabilities_service.get_tutor_availabilities(tutor_id)


@availabilities_router.post("/availabilities", response_model=AvailabilityHours)
async def create_tutor_availability(request: AvailabilityHours,
                                    _user_response: UserResponse = Depends(authenticate_user)) -> AvailabilityHours:
    """
    Create a new availability time slot for a current tutor

    Args:
        request (AvailabilityHours): Time slot data to be added
        _user_response (UserResponse): The currently authenticated user

    Returns:
        AvailabilityHours: Added record of AvailabilityHours
    """
    return await availabilities_service.create_tutor_availability(_user_response.user.id, request)


@availabilities_router.post("/unavailabilities/", response_model=UnavailabilityHours)
async def create_tutor_unavailability(request: UnavailabilityHours,
                                      _user_response: UserResponse = Depends(authenticate_user)) -> UnavailabilityHours:
    """
    Create a new unavailability time slot for a current tutor

    Args:
        request (UnavailabilityHours): Time slot data to be added
        _user_response (UserResponse): The currently authenticated user

    Returns:
        UnavailabilityHours: Added record of UnavailabilityHours
    """
    return await availabilities_service.create_tutor_unavailability(_user_response.user.id, request)
