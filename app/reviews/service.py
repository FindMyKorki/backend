from crud.crud_provider import CRUDProvider
from .dataclasses import Review, UpsertReview


crud_provider = CRUDProvider("reviews")


class ReviewService:
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

