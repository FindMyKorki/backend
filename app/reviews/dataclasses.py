from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Review(BaseModel):
    id: str  # Changed to uuid (str)
    created_at: datetime
    booking_id: str  # Changed to uuid (str)
    student_id: str  # Renamed from user_id to student_id
    tutor_id: str  # Renamed from tutor_profile_id to tutor_id
    rating: int
    comment: str  # Removed Optional, made it required

    class Config:
        from_attributes = True


class CreateReview(BaseModel):
    booking_id: str  # Changed to uuid (str)
    student_id: str  # Renamed from user_id to student_id
    tutor_id: str  # Renamed from tutor_profile_id to tutor_id
    rating: int
    comment: str  # Removed Optional, made it required

    class Config:
        from_attributes = True


class UpdateReview(BaseModel):
    rating: int
    comment: str

    class Config:
        from_attributes = True