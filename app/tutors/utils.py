from core.db_connection import supabase
from fastapi import HTTPException


async def get_tutor_profile_data(tutor_id: str):
    """Get tutor profile data from the database"""
    tutor = (
        supabase.table('tutor_profiles')
        .select("*, profiles(full_name, avatar_url), reviews!tutor_profiles_featured_review_id_fkey(id, student_id, tutor_id, rating, comment, created_at)")
        .eq("id", tutor_id)
        .execute()
    )

    if tutor.data and len(tutor.data) > 0:
        return flatten_tutor_data(tutor.data[0])

    return None


def flatten_tutor_data(tutor_data: dict):
    """Transform nested tutor profile data into a flat structure"""
    profile = tutor_data.get("profiles", {}) or {}
    featured_review = tutor_data.get("reviews", {}) or {}

    return {
        "id": tutor_data["id"],
        "bio": tutor_data["bio"],
        "bio_long": tutor_data.get("bio_long"),
        "rating": tutor_data["rating"],
        "contact_email": tutor_data.get("contact_email"),
        "phone_number": tutor_data.get("phone_number"),
        "featured_review": {
            "id": featured_review.get("id"),
            "student_id": featured_review.get("student_id"),
            "tutor_id": featured_review.get("tutor_id"),
            "rating": featured_review.get("rating"),
            "comment": featured_review.get("comment"),
            "created_at": featured_review.get("created_at"),
        } if featured_review else None,
        "full_name": profile.get("full_name"),
        "avatar_url": profile.get("avatar_url"),
    }