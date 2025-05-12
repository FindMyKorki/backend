from datetime import datetime
from pydantic import BaseModel, EmailStr
from subjects.dataclasses import Subject
from typing import Optional


class OfferInterface(BaseModel):
    id: int
    price: Optional[float] = None
    subject_name: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    icon_url: Optional[str] = None
    level: Optional[str] = None

    class Config:
        from_attributes = True


class OfferResponse(OfferInterface):
    tutor_full_name: str
    tutor_avatar_url: Optional[str] = None
    tutor_rating: Optional[float] = None


class UpdateOfferRequest(BaseModel):
    subject_id: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None
    level_id: int


class TutorOfferResponse(OfferInterface):
    is_active: bool


class ActiveOfferResponse(OfferInterface):
    tutor_full_name: str
    tutor_avatar_url: Optional[str] = None
    tutor_rating: Optional[float] = None


# CRUD
class Level(BaseModel):
    id: int
    level: str

    class Config:
        from_attributes = True


class BaseOffer(BaseModel):
    price: Optional[float]
    title: Optional[str]
    description: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class Offer(BaseOffer):
    id: int
    tutor_id: str
    subject: Optional[Subject]
    created_at: datetime
    level: Optional[Level]


class CreateOffer(BaseOffer):
    subject_id: Optional[int]
    level_id: Optional[int]


class UpdateOffer(CreateOffer):
    id: int
