from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class Review(BaseModel):
    id: int
    created_at: datetime
    booking_id: int
    user_id: int
    tutor_profile_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class CreateReview(BaseModel):
    booking_id: int
    user_id: int
    tutor_profile_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateReview(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

    class Config:
        from_attributes = True