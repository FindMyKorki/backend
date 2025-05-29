from fastapi import APIRouter, Depends, Path, Query
from gotrue.types import UserResponse
from users.auth import authenticate_user

from .dataclasses import AvailabilityHours, UnavailabilityHours, AvailabilityResponse, UnavailabilityResponse
from .service import AvailabilityService

availabilities_router = APIRouter()
availabilities_service = AvailabilityService()


@availabilities_router.get("/availabilities/{tutor_id}", response_model=list[AvailabilityResponse])
async def get_tutor_availabilities(tutor_id: str = Path(...)) -> list[AvailabilityResponse]:
    """
    Get a list of availability slots for a specific tutor

    Args:
        tutor_id (str): Tutor UUID

    Returns:
        List[AvailabilityResponse]: A list of time slots when the tutor is available
    """
    return await availabilities_service.get_tutor_availabilities(tutor_id)

@availabilities_router.get("/availabilities", response_model=list[AvailabilityResponse])
async def get_tutor_availabilities(_user_response = Depends(authenticate_user)) -> list[AvailabilityResponse]:
    """
    Get a list of availability slots for a specific tutor

    Args:
        _user_response: currently authenticated user

    Returns:
        List[AvailabilityResponse]: A list of time slots when the tutor is available
    """
    return await availabilities_service.get_tutor_availabilities(_user_response.user.id)

@availabilities_router.get("/unavailabilities", response_model=list[UnavailabilityResponse])
async def get_tutor_unavailabilities(_user_response = Depends(authenticate_user)) -> list[UnavailabilityHours]:
    """
        Get a list of unavailabilities for logged in tutor

        Args:
            _user_response: currently authenticated user

        Returns:
            List[UnavailabilityResponse]: A list of unavailabilities
        """
    return await availabilities_service.get_tutor_unavailabilities(_user_response.user.id)

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

@availabilities_router.delete("/availabilities/{availability_id}")
async def delete_tutor_availability(availability_id: int = Path(...), _user_response: UserResponse = Depends(authenticate_user)):
    """
    Delete an existing availability that belongs to currently logged in tutor

    Args:
        availability_id (int): id of availability that you want to remove
        _user_response (UserResponse): The currently authenticated user

    Returns:
        Deleted availability data
    """
    return await availabilities_service.delete_availability(availability_id, _user_response.user.id)


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

@availabilities_router.delete("/unavailabilities/{unavailability_id}")
async def delete_tutor_availability(unavailability_id: int = Path(...), _user_response: UserResponse = Depends(authenticate_user)):
    """
    Delete an existing availability that belongs to currently logged in tutor

    Args:
        unavailability_id (int): id of unavailability that you want to remove
        _user_response (UserResponse): The currently authenticated user

    Returns:
        Deleted unavailability data
    """
    return await availabilities_service.delete_unavailability(unavailability_id, _user_response.user.id)