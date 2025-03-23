from core.db_connection import supabase
from fastapi import HTTPException, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from gotrue.types import UserResponse


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def authenticate_user(access_token: Annotated[str, Depends(oauth2_scheme)]) -> UserResponse:
    try:
        response = supabase.auth.get_user(access_token)
        return response
    except:
        raise HTTPException(status_code=401, detail='User unauthorized')

async def authenticate_sign_out(access_token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        supabase.auth.get_user(access_token)
        return access_token
    except:
        raise HTTPException(status_code=401, detail='User unauthorized')

async def authorize_user():
    pass
