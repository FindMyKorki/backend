from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import TutorResponse


async def get_tutor_profile_data(tutor_id: str) -> TutorResponse:
    tutor = (
        supabase.table('tutor_profiles')
        .select(
            "id, bio, bio_long, rating, contact_email, phone_number, profiles(full_name, avatar_url), reviews!tutor_profiles_featured_review_id_fkey(id, student_id, tutor_id, rating, comment, created_at)")
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
        "featured_review_id": tutor_data["reviews"].get("id") if tutor_data.get("reviews") else None,
        "featured_review_rating": tutor_data["reviews"].get("rating") if tutor_data.get("reviews") else None,
        "featured_review_comment": tutor_data["reviews"].get("comment") if tutor_data.get("reviews") else None,
        "full_name": tutor_data["profiles"].get("full_name") if tutor_data.get("profiles") else None,
        "avatar_url": tutor_data["profiles"].get("avatar_url") if tutor_data.get("profiles") else None,
    }
