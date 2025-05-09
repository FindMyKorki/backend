import os
from fastapi import APIRouter, Request, Depends, Path

from .auth import authenticate_sign_out, authenticate_user
from .dataclasses import RefreshTokensRequest, CodeForSessionResponse, TokensResponse, SignInResponse, CallbackResponse, \
    CreateUserRequest, UserResponse, UpdateUserRequest, MyUserResponse
from .service import UsersService

users_router = APIRouter()
users_service = UsersService()


@users_router.get('/auth/sign-in/{provider}', response_model=SignInResponse)
async def sign_in(provider: str = Path(...), redirect_to: str = '/auth/callback'):
    return await users_service.sign_in(provider, redirect_to)


@users_router.get('/auth/callback', response_model=CallbackResponse)
async def auth_callback(request: Request):
    return await users_service.auth_callback(request)


@users_router.get('/auth/exchange-code-for-session/{code}/{code_verifier}', response_model=CodeForSessionResponse)
async def exchange_code_for_session(code: str = Path(...), code_verifier: str = Path(...)):
    return await users_service.exchange_code_for_session(code, code_verifier)


@users_router.post('/auth/sign-out', response_model=None)
async def sign_out(access_token=Depends(authenticate_sign_out)):
    return await users_service.sign_out(access_token)


@users_router.post('/auth/refresh-tokens', response_model=TokensResponse)
async def refresh_tokens(request: RefreshTokensRequest):
    return await users_service.refresh_tokens(request)


# New endpoints below

@users_router.get('/user')
async def get_user(_user_response=Depends(authenticate_user)) -> MyUserResponse:
    """
    Retrieve the current authenticated user's information.

    Args:
        _user_response (UserResponse): The authenticated user details from the authentication service.

    Returns:
        MyUserResponse: The details of the authenticated user.
    """
    return await users_service.get_self(_user_response)


@users_router.get('/users/{user_id}', response_model=UserResponse)
async def get_user(user_id: str = Path(...)):
    """
    Get a user by their unique identifier (ID).

    Args:
        user_id (str): The UUID of the user whose information is being requested.

    Returns:
        UserResponse: The details of the requested user.
    """
    return await users_service.get_user(user_id)


@users_router.put('/users/profile', response_model=UserResponse)
async def update_user(request: UpdateUserRequest, _user_response=Depends(authenticate_user)):
    """
    Update the current authenticated user's profile information.

    Args:
        request (UpdateUserRequest): The new information to update the user's profile.
        _user_response (UserResponse): The authenticated user details.

    Returns:
        UserResponse: The updated details of the user.
    """
    user_id = _user_response.user.id
    return await users_service.update_user(user_id, request)


@users_router.post('/users/delete', response_model=str)
async def delete_user(_user_response=Depends(authenticate_user)):
    """
    Delete the current authenticated user's account.

    Args:
        _user_response (UserResponse): The authenticated user details.

    Returns:
        str: A confirmation message indicating the user was successfully deleted.
    """
    user_id = _user_response.user.id
    return await users_service.delete_user(user_id)
