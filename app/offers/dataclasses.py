from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Offer(BaseModel):
    id: int
    created_at: datetime
    tutor_profile_id: int
    title: str
    description: str
    subject: str
    price: float
    duration: int  # Duration in minutes
    is_active: bool

    class Config:
        from_attributes = True


class CreateOffer(BaseModel):
    tutor_profile_id: int
    title: str
    description: str
    subject: str
    price: float
    duration: int  # Duration in minutes
    is_active: bool = True

    class Config:
        from_attributes = True


class UpdateOffer(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[int] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True