from fastapi import APIRouter, Depends
from users.auth import authenticate_user

from .dataclasses import TutorProfile, UpdateTutorProfile, TutorResponse
from .service import TutorsService

tutors_router = APIRouter()
tutors_service = TutorsService()


@tutors_router.put("/tutors", response_model=TutorProfile)
async def update_tutor_profile(update_data: UpdateTutorProfile, user_response=Depends(authenticate_user)):
    """Update a tutor's profile information"""
    tutor_id = user_response.user.id
    return await tutors_service.update_tutor_profile(tutor_id, update_data)


@tutors_router.post('/tutors', response_model=str)
async def create_tutor_profile(request: UpdateTutorProfile, _user_response=Depends(authenticate_user)) -> str:
    """
    Create a new tutor profile for a specific user.

    Args:
        request (UpdateTutorProfile): Data required to set up the tutor profile (bio, contact_email, phone_number).
        _user_response (str): UserResponse from authenticate_user().

    Returns:
        str: Confirmation message or the ID of the newly created tutor profile.
    """
    return await tutor_service.create_tutor_profile(request, _user_response.user.id)


@tutors_router.get('/tutors/{tutor_id}', response_model=TutorResponse)
async def get_tutor_profile(tutor_id: str) -> TutorResponse:
    """
    Retrieve the profile of a specific tutor by their UUID.

    Args:
        tutor_id (str): Tutor UUID.

    Returns:
        TutorResponse: Full details of the tutor profile (bio, contact_email, phone_number, rating, featured_review_id, full_name, avatar_url).
    """
    return await tutor_service.get_tutor_profile(tutor_id)
