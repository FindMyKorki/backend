from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import TutorResponse


async def get_tutor_profile_data(tutor_id: str) -> TutorResponse:
    tutor = (
        supabase.table('tutor_profiles')
        .select(
            "id, bio, bio_long, rating, contact_email, phone_number, featured_review_id, profiles(full_name, avatar_url)")
        .eq("id", tutor_id)
        .execute()
    )

    if tutor.data and len(tutor.data) > 0:
        return flatten_tutor_data(tutor.data[0])

    return None


def flatten_tutor_data(tutor_data: {}) -> TutorResponse:
    return {
        "bio": tutor_data["bio"],
        "bio_long": tutor_data["bio_long"],
        "rating": tutor_data["rating"],
        "contact_email": tutor_data["contact_email"],
        "phone_number": tutor_data["phone_number"],
        "featured_review_id": tutor_data["featured_review_id"],
        "full_name": tutor_data["profiles"].get("full_name") if tutor_data.get("profiles") else None,
        "avatar_url": tutor_data["profiles"].get("avatar_url") if tutor_data.get("profiles") else None,
    }
