from fastapi import APIRouter, Depends, Path
from gotrue.types import UserResponse
from users.auth import authenticate_user

from .dataclasses import StudentReview
from .service import StudentReviewsService

student_reviews_router = APIRouter()
student_reviews_service = StudentReviewsService()


@student_reviews_router.get("/student-reviews", response_model=list[StudentReview])
async def get_student_reviews(_user_response: UserResponse = Depends(authenticate_user)):
    """
    Retrieve all reviews associated with a specific student.

    Args:
        _user_response (UserResponse): The authenticated user making the request.

    Returns:
        list[StudentReview]: A list of reviews left for the specified student.
    """
    return await student_reviews_service.get_student_reviews(_user_response.user.id)

