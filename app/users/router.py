from .service import UserService
from fastapi import APIRouter, Request


users_router = APIRouter()
users_service = UserService()

@users_router.get('/auth/sign-in')
async def sign_in(provider: str):
    return await users_service.auth_provider(provider, '/auth/callback')

@users_router.get('/auth/callback')
async def auth_callback(request: Request):
    return await users_service.auth_callback(request)

@users_router.post('/auth/sign-out')
async def sign_out():
    return await users_service.sign_out()
