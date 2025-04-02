from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateTutorProfileRequest(BaseModel):
    bio: str
    contact_email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True


class TutorResponse(BaseModel):
    bio: str
    rating: float
    contact_email: Optional[str] = None
    phone_number: Optional[str] = None
    featured_review_id: Optional[str] = None  # featured_review id
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True
