from fastapi import APIRouter, Depends
from users.auth import authenticate_user

from .dataclasses import StudentReview
from .service import StudentReviewsService

student_reviews_router = APIRouter()
student_reviews_service = StudentReviewsService()


@student_reviews_router.get("/student-reviews/{student_id}", response_model=list[StudentReview])
async def get_student_reviews(student_id: str, user_response=Depends(authenticate_user)):
    """Get all reviews for a student"""
    return await student_reviews_service.get_student_reviews(student_id)
