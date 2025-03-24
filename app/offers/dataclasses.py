from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Offer(BaseModel):
    id: str
    created_at: datetime
    tutor_id: str
    subject_id: str
    price: float
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True


class Subjects(BaseModel):
    id: str
    subject: str


class OfferLevel(BaseModel):
    offer_id: str
    level_id: str