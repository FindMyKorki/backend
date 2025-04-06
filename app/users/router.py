from .service import UsersService
from .dataclasses import RefreshTokensRequest, CodeForSessionResponse, TokensResponse, SignInResponse, CallbackResponse, CreateUserRequest, UserResponse, UpdateUserRequest
from .auth import authenticate_sign_out, authenticate_user
from fastapi import APIRouter, Request, Depends


users_router = APIRouter()
users_service = UsersService()

@users_router.get('/auth/sign-in/{provider}', response_model=SignInResponse)
async def sign_in(provider: str):
    return await users_service.sign_in(provider, '/auth/callback')

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

# New endpoints below

@users_router.post('/users', response_model=UserResponse)
async def create_user(request: CreateUserRequest):
    """Create a new user"""
    return await users_service.create_user(request)

@users_router.get('/users/{user_id}', response_model=UserResponse)
async def get_user(user_id: str):
    """Get a user by ID"""
    return await users_service.get_user(user_id)

@users_router.put('/users/{user_id}', response_model=UserResponse)
async def update_user(user_id: str, request: UpdateUserRequest, user_response=Depends(authenticate_user)):
    """Update a user's information"""
    return await users_service.update_user(user_id, request)

@users_router.post('/users/{user_id}:delete', response_model=str)
async def delete_user(user_id: str, user_response=Depends(authenticate_user)):
    """Delete a user"""
    return await users_service.delete_user(user_id)