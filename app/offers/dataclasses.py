from pydantic import BaseModel, EmailStr
from typing import Optional


class OfferResponse(BaseModel):
    id: int
    description: Optional[str] = None
    tutor_full_name: str
    tutor_url: Optional[str] = None  # Na razie `None`
    tutor_rating: Optional[float] = None
    price: Optional[float] = None
    subject_name: Optional[str] = None
    level: Optional[str] = None
    icon_url: Optional[str] = None


class UpdateOfferRequest(BaseModel):
    subject_id: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None
    level_id: int


class TutorOfferResponse(BaseModel):
    """GET /tutor-offers/{tutor_id}

    return: list of TutorOfferResponse
    {
    id: text,
    price: text,
    subject_name: text,
    icon_url: text,
    level: text,
    is_true: bool
    }"""
    id: int
    price: Optional[float] = None
    subject_name: Optional[str] = None
    icon_url: Optional[str] = None
    level: Optional[str] = None
    is_active: bool