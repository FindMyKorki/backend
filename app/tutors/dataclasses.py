from pydantic import BaseModel, EmailStr
from typing import Optional


class TutorProfile(BaseModel):
    id: str
    bio: str
    bio_long: Optional[str] = None
    rating: float
    contact_email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    featured_review_id: Optional[int] = None
    avatar_url: Optional[str] = None
    full_name: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateTutorProfile(BaseModel):
    bio: Optional[str] = None
    bio_long: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True