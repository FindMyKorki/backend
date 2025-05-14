import os
from core.db_connection import supabase, SUPABASE_KEY, SUPABASE_URL
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from profiles.utils import get_profile_data
from supabase import AuthApiError, create_client, Client

from .dataclasses import CodeForSessionResponse, TokensResponse, RefreshTokensRequest, SignInResponse, CallbackResponse, \
    CreateUserRequest, UserResponse, UpdateUserRequest, MyUserResponse, MyProfileResponse, MyTutorProfileResponse, \
    FeaturedReview


class UsersService:
    async def sign_in(self, provider: str, redirect_to: str) -> SignInResponse:
        backend_url = os.getenv("BACKEND_URL")
        if provider in ['google', 'facebook']:
            response = supabase.auth.sign_in_with_oauth(
                {
                    'provider': provider,
                    'options': {
                        'redirect_to': f"{backend_url}{redirect_to}"
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
        frontend_url = os.getenv("FRONTEND_URL")
        if frontend_url:
            url = os.getenv("FRONTEND_URL") + "?code=" + code
            return RedirectResponse(url)
        else:
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


    async def get_self(self, user_response):
        try:
            id = user_response.user.id

            user = MyUserResponse(
                id=id,
                provider_email=user_response.user.user_metadata.get("email"),
                provider_avatar_url=user_response.user.user_metadata.get("avatar_url"),
                provider_display_name=user_response.user.user_metadata.get("full_name")
            )

            profile = await get_profile_data(id)

            if profile:
                user.profile = MyProfileResponse(
                    full_name=profile.get("full_name"),
                    is_tutor=profile.get("is_tutor"),
                    avatar_url=profile.get("avatar_url")
                )

                if profile.get("is_tutor"):
                    tutor_profile = (
                        supabase.table("tutor_profiles")
                        .select(
                            "*, reviews!tutor_profiles_featured_review_id_fkey(id, student_id, tutor_id, rating, comment, created_at)")
                        .eq("id", id)
                        .execute()
                    )

                    if not tutor_profile.data or len(tutor_profile.data) == 0:
                        return user

                    user.tutor_profile = MyTutorProfileResponse(
                        bio=tutor_profile.data[0].get("bio"),
                        bio_long=tutor_profile.data[0].get("bio_long"),
                        rating=tutor_profile.data[0].get("rating"),
                        contact_email=tutor_profile.data[0].get("contact_email"),
                        phone_number=tutor_profile.data[0].get("phone_number"),
                    )

                    if not tutor_profile.data[0].get("featured_review_id"):
                        return user

                    user.tutor_profile.featured_review = FeaturedReview(
                        id=tutor_profile.data[0].get("reviews").get("id"),
                        comment=tutor_profile.data[0].get("reviews").get("comment"),
                        rating=tutor_profile.data[0].get("reviews").get("rating"),
                        student_id=tutor_profile.data[0].get("reviews").get("student_id")
                    )

            return user

        except AuthApiError as e:
            raise HTTPException(status_code=404, detail="User not found")

    def _create_client(self) -> Client:
        return create_client(
            SUPABASE_URL,
            SUPABASE_KEY,
        )
