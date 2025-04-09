from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateTutorProfileRequest(BaseModel):
    bio: Optional[str] = None
    bio_long: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True


class TutorResponse(CreateTutorProfileRequest):
    rating: float
    featured_review_id: Optional[int] = None  # featured_review id
    featured_review_rating: Optional[float] = None  # featured_review id
    featured_review_comment: Optional[str] = None  # featured_review id
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
