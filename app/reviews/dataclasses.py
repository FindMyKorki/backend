from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TutorReviewResponse(BaseModel):
    id: int
    rating: Optional[int]
    comment: str
    created_at: datetime
    student_id: str
    student_full_name: str
    student_avatar_url: Optional[str] = None


class UpsertReview(BaseModel):
    student_id: str
    tutor_id: str
    rating: Optional[int] = None
    comment: str

    class Config:
        from_attributes = True

class CreateReviewRequest(BaseModel):
    tutor_id: str
    comment: str
    rating: int

class Review(UpsertReview):
    id: int
    created_at: str
