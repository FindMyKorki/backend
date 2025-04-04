from fastapi import APIRouter, Depends, Path, Query
from users.auth import authenticate_user

from .dataclasses import TutorReviewResponse
from .service import ReviewsService

reviews_router = APIRouter()
reviews_service = ReviewsService()


@reviews_router.get("/tutor-reviews/{tutor_id}", response_model=list[TutorReviewResponse])
async def get_tutor_reviews(tutor_id: str) -> list[TutorReviewResponse]:
    return await reviews_service.get_tutor_reviews(tutor_id)
