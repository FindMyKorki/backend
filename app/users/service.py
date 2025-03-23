from .dataclasses import AuthCallbackResponse, TokensResponse, RefreshTokensRequest
from profiles.utils import get_profile_data
from core.db_connection import supabase
from fastapi import HTTPException, Request
from supabase import AuthApiError
from gotrue import OAuthResponse


class UsersService:
    async def sign_in(self, provider: str, redirect_to: str) -> OAuthResponse:
        if provider in ['google', 'facebook']:
            response = supabase.auth.sign_in_with_oauth(
                {
                    'provider': provider, 
                    'options': {
                        'redirect_to': redirect_to
                    }
                })
            
            return response

        raise HTTPException(status_code=404, detail='Provider not found')
    
    async def sign_out(self, access_token: str) -> None:
        response = supabase.auth.admin.sign_out(access_token)
        return response
    
    async def auth_callback(self, request: Request) -> AuthCallbackResponse:   
        code = request.query_params.get('code')

        try:
            session = supabase.auth.exchange_code_for_session({'auth_code': code})
        except:
            raise HTTPException(status_code=404, detail='Session not found')
    
        try:
            session_data = session.session
            access_token = session_data.access_token
            refresh_token = session_data.refresh_token

            user_response = supabase.auth.get_user(access_token)
            user_id = user_response.user.id

            self._remove_session()

            profile = await get_profile_data(user_id)
            return { 
                'tokens': 
                    {
                        'access_token': access_token, 
                        'refresh_token': refresh_token
                    }, 
                'profile': profile
            }
        except:
            raise HTTPException(status_code=404, detail='Session not found')

    async def refresh_tokens(self, request: RefreshTokensRequest) -> TokensResponse:
        try:
            response = supabase.auth.refresh_session(request.refresh_token)
            self._remove_session()
            
            return {
                'access_token': response.session.access_token,
                'refresh_token': response.session.refresh_token
            }
        except AuthApiError as e:
            raise HTTPException(status_code=401, detail=e.message)

    def _remove_session(self) -> None:
        supabase.auth._remove_session()
        supabase.auth._notify_all_subscribers("SIGNED_OUT", None)
    