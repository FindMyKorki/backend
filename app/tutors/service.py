from .dataclasses import CreateTutorProfileRequest, TutorResponse
from .utils import get_tutor_profile_data
from fastapi import HTTPException
from core.db_connection import supabase


class TutorService:
    async def create_tutor_profile(self, user_id: str, request: CreateTutorProfileRequest) -> int:
        tutor_profile = await get_tutor_profile_data(user_id)

        if tutor_profile:
            raise HTTPException(409, 'Tutor profile already exists')

        new_profile = (
            supabase.table('tutor_profiles')
            .insert({
                'id': user_id,
                'bio': request.bio,
                'rating': 0,  # Domyślna wartość oceny
                'contact_email': request.contact_email,
                'phone_number': request.phone_number,
                'featured_review_id': None  # Domyślnie brak wyróżnionej opinii
            })
            .execute()
        )

        return user_id

    async def get_tutor_profile(self, tutor_id: str):
        tutor_profile = await get_tutor_profile_data(tutor_id)

        if not tutor_profile:
            raise HTTPException(404, 'Tutor profile not found')

        return tutor_profile
