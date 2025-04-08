from fastapi import APIRouter, Depends
from users.auth import authenticate_user
from .service import TutorsService
from .dataclasses import TutorProfile, UpdateTutorProfile


tutors_router = APIRouter()
tutors_service = TutorsService()


@tutors_router.put("/tutors", response_model=TutorProfile)
async def update_tutor_profile(user_response=Depends(authenticate_user), update_data: UpdateTutorProfile):
    """Update a tutor's profile information"""
    tutor_id = user_response.profile.id
    return await tutors_service.update_tutor_profile(tutor_id, update_data)