from fastapi import APIRouter, Depends, Path, Query
from users.auth import authenticate_user

from .dataclasses import TutorReviewResponse
from .service import ReviewsService, SortBy, Order

reviews_router = APIRouter()
reviews_service = ReviewsService()


@reviews_router.get("/tutor-reviews/{tutor_id}", response_model=list[TutorReviewResponse])
async def get_tutor_reviews(tutor_id: str = Path(...),
                            sort_by: SortBy = Query(...),
                            order: Order = Query(...)) -> list[TutorReviewResponse]:
    """
    Retrieve all reviews for a specific tutor.

    Args:
        tutor_id (str): Tutor UUID.
        sort_by (SortBy): Field to sort offers by rating, date.
        order (Order): Sorting order increasing or decreasing.

    Returns:
        List[TutorReviewResponse]: A list of reviews for the specified tutor.
    """
    return await reviews_service.get_tutor_reviews(tutor_id, sort_by, order)
