from core.db_connection import supabase
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from gotrue.types import UserResponse
from profiles.dataclasses import Profile
from profiles.utils import get_profile_data
from typing import Annotated

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
oauth2_scheme = HTTPBearer()


async def authenticate_user(auth_header: Annotated[str, Depends(oauth2_scheme)]) -> UserResponse:
    # return access_token
    return await _authenticate_user(auth_header.credentials)


async def authenticate_profile(auth_header: Annotated[str, Depends(oauth2_scheme)]) -> Profile:
    try:
        access_token = auth_header.credentials
        user_data = await _authenticate_user(access_token)
        profile = await get_profile_data(user_data.user.id)

        if not profile:
            raise Exception

        return profile
    except:
        raise HTTPException(status_code=401, detail='User unauthorized')


async def authenticate_sign_out(auth_header: Annotated[str, Depends(oauth2_scheme)]) -> str:
    access_token = auth_header.credentials
    await _authenticate_user(access_token)
    return access_token


async def _authenticate_user(access_token: str) -> UserResponse:
    try:
        user_data = supabase.auth.get_user(access_token)
        return user_data
    except:
        raise HTTPException(status_code=401, detail='User unauthorized')
