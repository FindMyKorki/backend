from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Offer(BaseModel):
    id: str  # uuid
    created_at: datetime
    tutor_id: str  # Changed from tutor_profile_id to tutor_id
    subject_id: str  # uuid
    price: float
    title: str
    description: Optional[str]  # Made optional as per comment

    class Config:
        from_attributes = True


class Subjects(BaseModel):
    id: str  # uuid
    subject: str


class OfferLevel(BaseModel):
    offer_id: str  # uuid
    level_id: str  # uuid