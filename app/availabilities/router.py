from fastapi import APIRouter, Depends, Path, Query
from users.auth import authenticate_user

from .dataclasses import AvailabilityHours, UnavailabilityHours
from .service import AvailabilityService

availabilities_router = APIRouter()
availabilities_service = AvailabilityService()


@availabilities_router.get("/availabilities/{tutor_id}", response_model=list[AvailabilityHours])
async def get_tutor_availabilities(tutor_id: str) -> list[AvailabilityHours]:
    return await availabilities_service.get_tutor_availabilities(tutor_id)


@availabilities_router.post("/availabilities/{tutor_id}", response_model=str)
async def create_tutor_availability(tutor_id: str, request: AvailabilityHours) -> str:
    return await availabilities_service.create_tutor_availability(tutor_id, request)


@availabilities_router.post("/unavailabilities/{tutor_id}", response_model=str)
async def create_tutor_unavailability(tutor_id: str, request: UnavailabilityHours) -> str:
    return await availabilities_service.create_tutor_unavailability(tutor_id, request)
