from pydantic import BaseModel, EmailStr
from typing import Optional


class FeaturedReview(BaseModel):
    id: int
    student_id: str
    tutor_id: str
    rating: int
    comment: str
    created_at: str


class UpdateTutorProfile(BaseModel):
    bio: Optional[str] = None
    bio_long: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True


class TutorProfile(UpdateTutorProfile):
    id: str
    rating: float
    featured_review: Optional[FeaturedReview] = None
    avatar_url: Optional[str] = None
    full_name: Optional[str] = None


class TutorResponse(UpdateTutorProfile):
    rating: float
    featured_review_id: Optional[int] = None
    featured_review_student_id: Optional[str] = None
    featured_review_student_fullname: Optional[str] = None
    featured_review_student_avatar_url: Optional[str] = None
    featured_review_rating: Optional[float] = None
    featured_review_comment: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    reviews_count: int
