from pydantic import BaseModel
from typing import Optional


class BaseTutorProfile(BaseModel):
    bio: Optional[str]
    contact_email: Optional[str]
    phone_number: Optional[str]
    featured_review_id: Optional[int]
    bio_long: Optional[str]

    class Config:
        from_attributes = True


class TutorProfile(BaseTutorProfile):
    id: str
    rating: Optional[float]
