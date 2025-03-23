from .service import UsersService
from .dataclasses import RefreshTokensRequest, AuthCallbackResponse, TokensResponse
from .auth import authenticate_sign_out
from fastapi import APIRouter, Request, Depends
from gotrue import OAuthResponse


users_router = APIRouter()
users_service = UsersService()

@users_router.get('/auth/sign-in/{provider}', response_model=OAuthResponse)
async def sign_in(provider: str):
    return await users_service.sign_in(provider, '/auth/callback')

@users_router.get('/auth/callback', response_model=AuthCallbackResponse)
async def auth_callback(request: Request):
    return await users_service.auth_callback(request)

@users_router.post('/auth/sign-out', response_model=None)
async def sign_out(access_token=Depends(authenticate_sign_out)):
    return await users_service.sign_out(access_token)

@users_router.post('/auth/refresh-tokens', response_model=TokensResponse)
async def refresh_tokens(request: RefreshTokensRequest):
    return await users_service.refresh_tokens(request)