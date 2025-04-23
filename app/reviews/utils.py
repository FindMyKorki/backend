from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import TutorReviewResponse


def flatten_tutor_reviews_data(data: list[dict]) -> list[TutorReviewResponse]:
    result = []
    for offer in data:
        profile = offer.pop("profiles", {}) or {}
        result.append(
            TutorReviewResponse(
                id=offer.get("id"),
                rating=offer.get("rating"),
                comment=offer.get("comment"),
                created_at=offer.get("created_at"),
                student_id=offer.get("student_id"),
                student_full_name=profile.get("full_name"),
                student_avatar_url=profile.get("avatar_url")
            )
        )

    return result
