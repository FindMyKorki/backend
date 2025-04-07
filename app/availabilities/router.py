from fastapi import APIRouter, Depends, Path, Query
from users.auth import authenticate_user

from .dataclasses import AvailabilityHours, UnavailabilityHours
from .service import AvailabilityService

availabilities_router = APIRouter()
availabilities_service = AvailabilityService()


@availabilities_router.get("/availabilities/{tutor_id}", response_model=list[AvailabilityHours])
async def get_tutor_availabilities(tutor_id: str) -> list[AvailabilityHours]:
    """
    Get a list of availability slots for a specific tutor

    Args:
        tutor_id (str): Tutor UUID

    Returns:
        List[AvailabilityHours]: A list of time slots when the tutor is available
    """
    return await availabilities_service.get_tutor_availabilities(tutor_id)


@availabilities_router.post("/availabilities/{tutor_id}", response_model=str)
async def create_tutor_availability(tutor_id: str, request: AvailabilityHours) -> str:
    """
    Create a new availability time slot for a tutor

    Args:
        tutor_id (str): Tutor UUID
        request (AvailabilityHours): Time slot data to be added

    Returns:
        str: Confirmation message
    """
    return await availabilities_service.create_tutor_availability(tutor_id, request)


@availabilities_router.post("/unavailabilities/{tutor_id}", response_model=str)
async def create_tutor_unavailability(tutor_id: str, request: UnavailabilityHours) -> str:
    """
    Create a new unavailability time slot for a tutor

    Args:
        tutor_id (str): Tutor UUID
        request (UnavailabilityHours): Time slot data to be added

    Returns:
        str: Confirmation message
    """
    return await availabilities_service.create_tutor_unavailability(tutor_id, request)
