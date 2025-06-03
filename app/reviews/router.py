from fastapi import APIRouter, Depends, Path, Query
from users.auth import authenticate_user

from .dataclasses import TutorReviewResponse, CreateReviewRequest, Review
from .service import ReviewsService, SortBy, Order
from users.dataclasses import UserResponse

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

@reviews_router.post("/reviews", response_model=Review)
async def review_tutor(request: CreateReviewRequest,
                       _user_response: UserResponse = Depends(authenticate_user)
                       ):
    """
        Create a review for tutor that you haven't reviewed yet.

        Args:
            request (CreateReviewRequest): request containing tutor_id, rating and comment.
            _user_response (UserResponse): currently logged in user.

        Returns:
            List[TutorReviewResponse]: A list of reviews for the specified tutor.
    """
    return await reviews_service.create_tutor_review(request, _user_response.user.id)

@reviews_router.delete("/reviews/{review_id}")
async def delete_review(review_id: int = Path(...),
                        _user_response: UserResponse = Depends(authenticate_user)):
    """
            Create a review for tutor that you haven't reviewed yet.

            Args:
                review_id (int): id that you want to delete
                _user_response (UserResponse): currently logged in user.

            Returns:
                List[TutorReviewResponse]: A list of reviews for the specified tutor.
    """
    return await reviews_service.delete_tutor_review(review_id, _user_response.user.id)