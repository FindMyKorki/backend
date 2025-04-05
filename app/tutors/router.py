from fastapi import APIRouter, Depends
from users.auth import authenticate_user

from .dataclasses import CreateTutorProfileRequest, TutorResponse
from .service import TutorService

tutor_router = APIRouter()
tutor_service = TutorService()


@tutor_router.post('/tutors/{user_id}', response_model=str)
async def create_tutor_profile(user_id: str, request: CreateTutorProfileRequest) -> str:
    return await tutor_service.create_tutor_profile(user_id, request)


@tutor_router.get('/tutors/{tutor_id}', response_model=TutorResponse)
async def get_tutor_profile(tutor_id: str) -> TutorResponse:
    return await tutor_service.get_tutor_profile(tutor_id)
