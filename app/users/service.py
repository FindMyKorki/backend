from .dataclasses import CodeForSessionResponse, TokensResponse, RefreshTokensRequest, SignInResponse, CallbackResponse
from profiles.utils import get_profile_data
from core.db_connection import supabase, SUPABASE_KEY, SUPABASE_URL
from fastapi import HTTPException, Request
from supabase import AuthApiError, create_client, Client


class UsersService:
    async def sign_in(self, provider: str, redirect_to: str) -> SignInResponse:
        if provider in ['google', 'facebook']:
            response = supabase.auth.sign_in_with_oauth(
                {
                    'provider': provider, 
                    'options': {
                        'redirect_to': redirect_to
                    }
                })
                        
            code_verifier = supabase.auth._storage.get_item(f'{supabase.auth._storage_key}-code-verifier')
            
            return SignInResponse(
                code_verifier=code_verifier, 
                oauth_response=response
                )
            
        raise HTTPException(status_code=404, detail='Provider not found')
    
    async def sign_out(self, access_token: str) -> None:
        response = supabase.auth.admin.sign_out(access_token)
        return response
    
    async def exchange_code_for_session(self, code: str, code_verifier: str) -> CodeForSessionResponse:
        session_client = self._create_client()

        try:
            session = session_client.auth.exchange_code_for_session(
                {
                    'auth_code': code, 
                    'code_verifier': code_verifier
                }
            )
        except:
            raise HTTPException(status_code=404, detail='Session not found')

        try:
            session_data = session.session
            access_token = session_data.access_token
            refresh_token = session_data.refresh_token

            user_response = supabase.auth.get_user(access_token)
            user_id = user_response.user.id

            profile = await get_profile_data(user_id)

            return CodeForSessionResponse(
                tokens=TokensResponse(
                    access_token=access_token, 
                    refresh_token=refresh_token
                    ), 
                profile=profile
                )
        except:
            raise HTTPException(status_code=404, detail='Session not found')
    
    async def auth_callback(self, request: Request) -> CallbackResponse:   
        code = request.query_params.get('code')

        return CallbackResponse(code=code)

    async def refresh_tokens(self, request: RefreshTokensRequest) -> TokensResponse:
        tokens_client = self._create_client()

        try:
            response = tokens_client.auth.refresh_session(request.refresh_token)
            
            return TokensResponse(
                access_token=response.session.access_token, 
                refresh_token=response.session.refresh_token
                )

        except AuthApiError as e:
            raise HTTPException(status_code=401, detail=e.message)
    
    def _create_client(self) -> Client:
        return create_client(
            SUPABASE_URL,
            SUPABASE_KEY,
        )