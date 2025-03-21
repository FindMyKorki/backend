from reviews.service import ReviewsService
from reviews.dataclasses import Review, CreateReview, UpdateReview

from fastapi import APIRouter, HTTPException, Path, Query, Response, status

reviews_router = APIRouter()
reviews_service = ReviewsService()


@reviews_router.get("/reviews", response_model=list[Review])
async def get_reviews():
    return await reviews_service.get_reviews()


@reviews_router.get("/review/{review_id}", response_model=Review)
async def get_review(review_id: int = Path(..., title="The ID of the review")):
    review = await reviews_service.get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@reviews_router.get("/booking/{booking_id}/review", response_model=Review)
async def get_booking_review(booking_id: int = Path(..., title="The ID of the booking")):
    review = await reviews_service.get_booking_review(booking_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found for this booking")
    return review


@reviews_router.get("/tutor/{tutor_profile_id}/reviews", response_model=list[Review])
async def get_tutor_reviews(tutor_profile_id: int = Path(..., title="The ID of the tutor profile")):
    return await reviews_service.get_tutor_reviews(tutor_profile_id)


@reviews_router.get("/user/{user_id}/reviews", response_model=list[Review])
async def get_user_reviews(user_id: int = Path(..., title="The ID of the user")):
    return await reviews_service.get_user_reviews(user_id)


@reviews_router.post("/review", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_review(create_review_data: CreateReview):
    # Check if a review already exists for this booking
    existing_review = await reviews_service.get_booking_review(create_review_data.booking_id)
    if existing_review:
        raise HTTPException(
            status_code=400,
            detail=f"A review already exists for booking {create_review_data.booking_id}"
        )

    return await reviews_service.create_review(create_review_data)


@reviews_router.put("/review/{review_id}", response_model=str)
async def update_review(
        update_data: UpdateReview,
        review_id: int = Path(..., title="The ID of the review to update")
):
    # Check if review exists
    review = await reviews_service.get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return await reviews_service.update_review(review_id, update_data)


@reviews_router.delete("/review/{review_id}", response_model=str, status_code=status.HTTP_200_OK)
async def delete_review(review_id: int = Path(..., title="The ID of the review to delete")):
    # Check if review exists
    review = await reviews_service.get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return await reviews_service.delete_review(review_id)