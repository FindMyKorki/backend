from core.db_connection import supabase
from profiles.utils import get_profile_data
from profiles.dataclasses import Profile
from fastapi import HTTPException, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from gotrue.types import UserResponse


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def authenticate_user(access_token: Annotated[str, Depends(oauth2_scheme)]) -> UserResponse:
    return await _authenticate_user(access_token)

async def authenticate_profile(access_token: Annotated[str, Depends(oauth2_scheme)]) -> Profile:
    try:
        user_data = await _authenticate_user(access_token)
        profile = await get_profile_data(user_data.user.id)
        
        if not profile:
            raise Exception
        
        return profile
    except:
        raise HTTPException(status_code=401, detail='User unauthorized')

async def authenticate_sign_out(access_token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    await _authenticate_user(access_token)
    return access_token

async def _authenticate_user(access_token: str) -> UserResponse:
    try:
        user_data = supabase.auth.get_user(access_token)
        return user_data
    except:
        raise HTTPException(status_code=401, detail='User unauthorized')