from fastapi import APIRouter, Depends
from users.auth import authenticate_user

from .dataclasses import CreateProfile, Profile
from .service import ProfilesService

profiles_router = APIRouter()
profiles_service = ProfilesService()


@profiles_router.post('/profiles', response_model=Profile)
async def create_profile(create_profile: CreateProfile, user_response=Depends(authenticate_user)) -> Profile:
    return await profiles_service.create_profile(create_profile, user_response.user.id)


@profiles_router.get('/profiles/{id}', response_model=Profile)
async def get_profile(id: str) -> Profile:
    return await profiles_service.get_profile(id)
