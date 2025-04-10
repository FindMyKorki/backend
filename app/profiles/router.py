from .service import ProfilesService
from .dataclasses import BaseProfile, Profile
from users.auth import authenticate_user
from fastapi import APIRouter, Depends


profiles_router = APIRouter()
profiles_service = ProfilesService()

@profiles_router.post('/profiles', response_model=Profile)
async def create_profile(create_profile: BaseProfile, user_response=Depends(authenticate_user)):
    return await profiles_service.create_profile(create_profile, user_response.user.id)

@profiles_router.get('/profiles/{id}', response_model=Profile)
async def get_profile(id: str):
    return await profiles_service.get_profile(id)