from typing import Optional, List

from fastapi import APIRouter, Depends, Path, UploadFile
from gotrue.types import UserResponse
from users.auth import authenticate_user

from .dataclasses import Profile, CreateProfileRequest, UpdateProfileRequest, SetRoleRequest, BaseProfile
from .service import ProfilesService, _parse_from_create_request, _parse_from_update_request
from users.dataclasses import MyUserResponse

profiles_router = APIRouter()
profiles_service = ProfilesService()

@profiles_router.post('/profiles', response_model=Profile)
async def create_profile(request: SetRoleRequest, _user_response: UserResponse = Depends(authenticate_user)):
    """
    Create new user profile with role specified by request.

    Args:
    request (SetRoleRequest): request containing information about desired user role
    _user_response (UserResponse): The authenticated user making the request.

    Returns:
        Profile: newly created profile containing id and is_tutor
    """
    return await profiles_service.setRole(_user_response, request)

# @profiles_router.put('/profiles', response_model=Profile)
# async def create_profile(avatar: List[UploadFile] = None,
#                          profile_data: CreateProfileRequest = Depends(_parse_from_create_request),
#                          _user_response: UserResponse = Depends(authenticate_user)):
#     """
#     Create a new user profile.
#
#     Args:
#         avatar (List[UploadFile]): Optional image file to be set as user's avatar
#         profile_data (CreateProfileRequest): The profile data to be saved.
#         _user_response (UserResponse): The authenticated user making the request.
#
#     Returns:
#         Profile: The newly created profile with its details.
#     """
#     return await profiles_service.create_profile(_user_response, profile_data, avatar)


@profiles_router.put('/profiles', response_model=BaseProfile)
async def update_profile(avatar: List[UploadFile] = None,
                         profile_data: UpdateProfileRequest = Depends(_parse_from_update_request),
                         _user_response: UserResponse = Depends(authenticate_user)):
    """
        Update a user profile. If no files are provided, don't put "avatar" argument in request.

        Args:
            avatar (List[UploadFile]): Optional image file to be set as user's new avatar
            profile_data (UpdateProfileRequest): The profile data to be saved, containing full_name and remove_avatar bool.
            _user_response (UserResponse): The authenticated user making the request.

        Returns:
            BaseProfile: Updated profile entry containing is_tutor, full_name and avatar_url
        """
    return await profiles_service.update_profile(_user_response, profile_data, avatar)

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
