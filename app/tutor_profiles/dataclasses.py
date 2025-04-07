from pydantic import BaseModel
from typing import Optional


class TutorProfile(BaseModel):
    id: str
    bio: Optional[str]
    rating: Optional[float]
    contact_email: Optional[str]
    phone_number: Optional[str]
    featured_review_id: Optional[int]
    bio_long: Optional[str]

    class Config:
        from_attributes = True


class UpsertTutorProfile(BaseModel):
    bio: Optional[str]
    contact_email: Optional[str]
    phone_number: Optional[str]
    featured_review_id: Optional[int]
    bio_long: Optional[str]

    class Config:
        from_attributes = True
