from fastapi import APIRouter, Depends, Path
from gotrue.types import UserResponse
from users.auth import authenticate_user

from .dataclasses import BaseProfile, Profile
from .service import ProfilesService

profiles_router = APIRouter()
profiles_service = ProfilesService()


@profiles_router.post('/profiles', response_model=Profile)
async def create_profile(create_profile: BaseProfile, _user_response: UserResponse = Depends(authenticate_user)):
    """
    Create a new user profile.

    Args:
        create_profile (BaseProfile): The profile data to be saved.
        _user_response (UserResponse): The authenticated user making the request.

    Returns:
        Profile: The newly created profile with its details.
    """
    return await profiles_service.create_profile(create_profile, _user_response.user.id)


@profiles_router.get('/profiles/{id}', response_model=Profile)
async def get_profile(id: str = Path(...)):
    """
    Retrieve a profile by its ID.

    Args:
        id (str): The UUID of the profile to retrieve.

    Returns:
        Profile: The full details of the requested user profile.
    """
    return await profiles_service.get_profile(id)
