from core.db_connection import supabase
from crud.crud_provider import CRUDProvider
from fastapi import HTTPException

from .dataclasses import TutorReviewResponse, Review, UpsertReview
from .utils import flatten_tutor_reviews_data

crud_provider = CRUDProvider("reviews")


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
            raise HTTPException(status_code=404, detail="No reviews found")

        return flatten_tutor_reviews_data(response.data)

    # CRUD
    async def create_review(self, review: UpsertReview, id: int = None) -> Review:
        new_review = await crud_provider.create(review.model_dump(exclude="created_at"), id)

        return Review.model_validate(new_review)

    async def get_review(self, id: int) -> Review:
        review = await crud_provider.get(id)

        return Review.model_validate(review)

    async def update_review(self, review: UpsertReview, id: int = None) -> Review:
        updated_review = await crud_provider.update(review.model_dump(exclude="created_at"), id)

        return Review.model_validate(updated_review)

    async def delete_review(self, id: int) -> Review:
        deleted_review = await crud_provider.delete(id)

        return Review.model_validate(deleted_review)
