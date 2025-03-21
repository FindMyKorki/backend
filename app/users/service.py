from core.db_connection import supabase
from fastapi import HTTPException, Request


class UserService:
    async def auth_provider(self, provider: str, redirect_to: str):
        if provider in ['google']:
            response = supabase.auth.sign_in_with_oauth(
                {
                    'provider': provider, 
                    'options': {
                        'redirect_to': redirect_to,
                    }
                })
            
            return response
        
        return HTTPException(status_code=404, detail='Provider not found')
    
    async def auth_callback(self, request: Request):
        code = request.query_params.get('code')
        session = supabase.auth.exchange_code_for_session({"auth_code": code})

        return session

    async def sign_out(self):
        response = supabase.auth.sign_out()
        return response
    