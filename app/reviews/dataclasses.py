from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Review(BaseModel):
    id: str
    created_at: datetime
    booking_id: str
    student_id: str
    tutor_id: str
    rating: int
    comment: str

    class Config:
        from_attributes = True


class CreateReview(BaseModel):
    booking_id: str
    student_id: str
    tutor_id: str
    rating: int
    comment: str

    class Config:
        from_attributes = True


class UpdateReview(BaseModel):
    rating: int
    comment: str

    class Config:
        from_attributes = True