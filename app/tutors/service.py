from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import TutorProfile, UpdateTutorProfile, TutorResponse
from .utils import get_tutor_profile_data


class TutorsService:
    async def update_tutor_profile(self, tutor_id: str, request: UpdateTutorProfile) -> TutorResponse:
        """Update tutor profile information"""
        # Check if tutor profile exists
        tutor_profile = await get_tutor_profile_data(tutor_id)

        if not tutor_profile:
            raise HTTPException(status_code=404, detail="Tutor profile not found")

        # Build update data dictionary with only provided fields
        update_data = {}
        if request.bio is not None:
            update_data["bio"] = request.bio
        if request.bio_long is not None:
            update_data["bio_long"] = request.bio_long
        if request.contact_email is not None:
            update_data["contact_email"] = request.contact_email
        if request.phone_number is not None:
            update_data["phone_number"] = request.phone_number

        # Only update if there's data to update
        if update_data:
            result = (
                supabase.table("tutor_profiles")
                .update(update_data)
                .eq("id", tutor_id)
                .execute()
            )

        # Return the updated profile
        updated_profile = await get_tutor_profile_data(tutor_id)
        return updated_profile

    async def create_tutor_profile(self, request: UpdateTutorProfile, user_id: str) -> str:
        if user_id is None:
            raise HTTPException(401, 'Unauthorized action')

        tutor_profile = await get_tutor_profile_data(user_id)

        if tutor_profile:
            raise HTTPException(409, 'Tutor profile already exists')

        new_profile = (
            supabase.table('tutor_profiles')
            .insert({
                'id': user_id,
                'bio': request.bio,
                'bio_long': request.bio_long,
                'rating': 0,  # Domyślna wartość oceny
                'contact_email': request.contact_email,
                'phone_number': request.phone_number,
                'featured_review_id': None  # Domyślnie brak wyróżnionej opinii
            })
            .execute()
        )

        return "Created tutor profile"

    async def get_tutor_profile(self, tutor_id: str) -> TutorResponse:
        tutor_profile = await get_tutor_profile_data(tutor_id)

        if not tutor_profile:
            raise HTTPException(404, 'Tutor profile not found')

        return tutor_profile
