from reviews.dataclasses import Review, CreateReview, UpdateReview
from core.db_connection import supabase


class ReviewsService:
    async def get_reviews(self) -> list[Review]:
        reviews = (
            supabase.table("reviews")
            .select("*")
            .execute()
        )
        return reviews.data

    async def get_review(self, review_id: int) -> Review:
        review = (
            supabase.table("reviews")
            .select("*")
            .eq("id", review_id)
            .execute()
        )
        return review.data[0] if review.data else None

    async def get_booking_review(self, booking_id: int) -> Review:
        review = (
            supabase.table("reviews")
            .select("*")
            .eq("booking_id", booking_id)
            .execute()
        )
        return review.data[0] if review.data else None

    async def get_tutor_reviews(self, tutor_profile_id: int) -> list[Review]:
        reviews = (
            supabase.table("reviews")
            .select("*")
            .eq("tutor_profile_id", tutor_profile_id)
            .execute()
        )
        return reviews.data

    async def get_user_reviews(self, user_id: int) -> list[Review]:
        reviews = (
            supabase.table("reviews")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return reviews.data

    async def create_review(self, create_review_data: CreateReview) -> str:
        new_review = (
            supabase.table("reviews")
            .insert(create_review_data.model_dump())
            .execute()
        )

        review_id = new_review.data[0].get("id")

        return f"Created new review with id {review_id}"

    async def update_review(self, review_id: int, update_data: UpdateReview) -> str:
        # Filter out None values
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

        if not update_dict:
            return "No fields to update"

        updated_review = (
            supabase.table("reviews")
            .update(update_dict)
            .eq("id", review_id)
            .execute()
        )

        return f"Updated review with id {review_id}"

    async def delete_review(self, review_id: int) -> str:
        deleted_review = (
            supabase.table("reviews")
            .delete()
            .eq("id", review_id)
            .execute()
        )

        return f"Deleted review with id {review_id}"