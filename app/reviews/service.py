from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import TutorReviewResponse
from .utils import flatten_tutor_reviews_data


class ReviewsService:
    async def get_tutor_reviews(self, tutor_id: str) -> list[TutorReviewResponse]:
        response = (
            supabase
            .table("reviews")
            .select(
                "id, rating, comment, created_at, student_id, "
                "profiles(full_name, avatar_url))"
            )
            .eq("tutor_id", tutor_id)
            .execute()
        )

        if response.data is None or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Offer not found")

        return flatten_tutor_reviews_data(response.data)
