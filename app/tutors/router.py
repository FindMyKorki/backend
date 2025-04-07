from fastapi import APIRouter, Depends
from users.auth import authenticate_user

from .dataclasses import CreateTutorProfileRequest, TutorResponse
from .service import TutorService

tutor_router = APIRouter()
tutor_service = TutorService()


@tutor_router.post('/tutors', response_model=str)
async def create_tutor_profile(request: CreateTutorProfileRequest, _user_response=Depends(authenticate_user)) -> str:
    """
    Create a new tutor profile for a specific user.

    Args:
        request (CreateTutorProfileRequest): Data required to set up the tutor profile (bio, contact_email, phone_number).
        _user_response (str): UserResponse from authenticate_user().

    Returns:
        str: Confirmation message or the ID of the newly created tutor profile.
    """
    return await tutor_service.create_tutor_profile(request, _user_response.user.id)


@tutor_router.get('/tutors/{tutor_id}', response_model=TutorResponse)
async def get_tutor_profile(tutor_id: str) -> TutorResponse:
    """
    Retrieve the profile of a specific tutor by their UUID.

    Args:
        tutor_id (str): Tutor UUID.

    Returns:
        TutorResponse: Full details of the tutor profile (bio, contact_email, phone_number, rating, featured_review_id, full_name, avatar_url).
    """
    return await tutor_service.get_tutor_profile(tutor_id)
