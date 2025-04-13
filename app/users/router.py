import os

from .service import UsersService
from .dataclasses import RefreshTokensRequest, CodeForSessionResponse, TokensResponse, SignInResponse, CallbackResponse
from .auth import authenticate_sign_out
from fastapi import APIRouter, Request, Depends


users_router = APIRouter()
users_service = UsersService()

@users_router.get('/auth/sign-in/{provider}', response_model=SignInResponse)
async def sign_in(provider: str):
    FRONTEND_SERVER_URL = os.getenv("FRONTEND_SERVER_URL")
    url = FRONTEND_SERVER_URL + "/auth/callback"
    return await users_service.sign_in(provider, url)

@users_router.get('/auth/callback', response_model=CallbackResponse)
async def auth_callback(request: Request):
    return await users_service.auth_callback(request)

@users_router.get('/auth/exchange-code-for-session/{code}/{code_verifier}', response_model=CodeForSessionResponse)
async def exchange_code_for_session(code: str, code_verifier :str):
    return await users_service.exchange_code_for_session(code, code_verifier)

@users_router.post('/auth/sign-out', response_model=None)
async def sign_out(access_token=Depends(authenticate_sign_out)):
    return await users_service.sign_out(access_token)

@users_router.post('/auth/refresh-tokens', response_model=TokensResponse)
async def refresh_tokens(request: RefreshTokensRequest):
    return await users_service.refresh_tokens(request)