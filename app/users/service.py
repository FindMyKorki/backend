from .dataclasses import CodeForSessionResponse, TokensResponse, RefreshTokensRequest, SignInResponse, CallbackResponse, CreateUserRequest, UserResponse, UpdateUserRequest
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
    
    async def create_user(self, request: CreateUserRequest) -> UserResponse:
        """Create a new user"""
        try:
            # Create user auth record
            user = supabase.auth.admin.create_user({
                "email": request.email,
                "password": request.password,
                "email_confirm": True  # Auto-confirm the email
            })
            
            user_id = user.user.id
            
            # If avatar_url is provided, create/update profile record
            if request.avatar_url:
                # Check if profile exists first
                profile_data = await get_profile_data(user_id)
                
                if profile_data:
                    # Update existing profile
                    supabase.table("profiles").update({
                        "avatar_url": request.avatar_url
                    }).eq("id", user_id).execute()
                else:
                    # Create new profile
                    supabase.table("profiles").insert({
                        "id": user_id,
                        "avatar_url": request.avatar_url
                    }).execute()
            
            return UserResponse(
                id=user.user.id,
                email=user.user.email,
                created_at=user.user.created_at,
                avatar_url=request.avatar_url
            )
            
        except AuthApiError as e:
            raise HTTPException(status_code=400, detail=e.message)
    
    async def get_user(self, user_id: str) -> UserResponse:
        """Get user by ID"""
        try:
            user = supabase.auth.admin.get_user_by_id(user_id)
            
            # Get profile data to fetch avatar_url
            profile = await get_profile_data(user_id)
            avatar_url = profile.avatar_url if profile else None
            
            return UserResponse(
                id=user.user.id,
                email=user.user.email,
                created_at=user.user.created_at,
                avatar_url=avatar_url
            )
            
        except AuthApiError as e:
            raise HTTPException(status_code=404, detail="User not found")
    
    async def update_user(self, user_id: str, request: UpdateUserRequest) -> UserResponse:
        """Update user information"""
        try:
            # Check if user exists
            user = supabase.auth.admin.get_user_by_id(user_id)

            # Do not update auth.users records
            avatar_url = None
            if request.avatar_url or request.full_name:
                # Check if profile exists
                profile_data = await get_profile_data(user_id)

                update_data = {}
                if request.avatar_url:
                    update_data["avatar_url"] = request.avatar_url
                if request.full_name:
                    update_data["full_name"] = request.full_name

                if profile_data:
                    # Update existing profile
                    supabase.table("profiles").update(update_data).eq("id", user_id).execute()
                else:
                    # Create new profile
                    update_data["id"] = user_id
                    supabase.table("profiles").insert(update_data).execute()

                avatar_url = update_data.get("avatar_url", None)
            else:
                # Get current avatar_url
                profile = await get_profile_data(user_id)
                if profile:
                    avatar_url = profile.avatar_url

            return UserResponse(
                id=user.user.id,
                email=user.user.email,
                created_at=user.user.created_at,
                avatar_url=avatar_url
            )

        except AuthApiError as e:
            if "not found" in str(e).lower():
                raise HTTPException(status_code=404, detail="User not found")
            raise HTTPException(status_code=400, detail=str(e))
    
    async def delete_user(self, user_id: str) -> str:
        """Delete a user by ID"""
        try:
            # Check if user exists
            supabase.auth.admin.get_user_by_id(user_id)
            
            # Delete user
            supabase.auth.admin.delete_user(user_id)
            
            return f"User {user_id} has been deleted"
            
        except AuthApiError as e:
            if "not found" in str(e).lower():
                raise HTTPException(status_code=404, detail="User not found")
            raise HTTPException(status_code=400, detail=str(e))
    
    def _create_client(self) -> Client:
        return create_client(
            SUPABASE_URL,
            SUPABASE_KEY,
        )