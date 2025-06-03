from core.db_connection import supabase
from crud.crud_provider import CRUDProvider
from enum import Enum
from fastapi import HTTPException

from .dataclasses import TutorReviewResponse, Review, UpsertReview, CreateReviewRequest
from .utils import flatten_tutor_reviews_data

crud_provider = CRUDProvider("reviews")


class SortBy(str, Enum):
    rating = "rating"
    date = "date"


class Order(str, Enum):
    increasing = "increasing"
    decreasing = "decreasing"


class ReviewsService:
    async def get_tutor_reviews(self, tutor_id: str, sort_by: str, order: str) -> list[TutorReviewResponse]:
        order_map = {
            SortBy.rating: "rating",
            SortBy.date: "created_at"
        }

        if sort_by not in order_map:
            raise HTTPException(status_code=400, detail="Invalid sort_by value")

        column = order_map[sort_by]
        sort_desc = order == Order.decreasing

        response = (
            supabase
            .table("reviews")
            .select(
                "id, rating, comment, created_at, student_id, "
                "profiles(full_name, avatar_url))"
            )
            .eq("tutor_id", tutor_id)
            .order(column, desc=sort_desc)
            .execute()
        )

        # if response.data is None or len(response.data) == 0:
        #     raise HTTPException(status_code=404, detail="No reviews found")

        return flatten_tutor_reviews_data(response.data)

    async def create_tutor_review(self, request: CreateReviewRequest, user_id: str) -> Review:
        tutor_id = request.tutor_id

        tutor_exists = supabase.table("tutor_profiles").select("id").eq("id", tutor_id).execute()
        if not tutor_exists.data:
            raise HTTPException(status_code=404, detail="Couldn't find tutor with that id")

        already_reviewed = supabase.table("reviews").select("*").eq("tutor_id", tutor_id).eq("student_id", user_id).execute()
        print(already_reviewed.data)
        if len(already_reviewed.data) > 0:
            raise HTTPException(status_code=409, detail="You already reviewed this tutor")

        if not (1 <= request.rating <= 5):
            raise ValueError("Rating must be a number between 1 and 5")

        review = UpsertReview(student_id = user_id, tutor_id = tutor_id, rating = request.rating, comment = request.comment)
        result = await self.create_review(review)

        return result

    async def delete_tutor_review(self, review_id: int, user_id: str) -> Review:
        review_exists = supabase.table("reviews").select("*").eq("id", review_id).eq("student_id", user_id).execute()
        if len(review_exists.data) == 0:
            raise HTTPException(status_code=404, detail="Your review with that id does not exist")

        return await self.delete_review(review_id)

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
