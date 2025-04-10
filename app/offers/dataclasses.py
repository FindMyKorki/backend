from pydantic import BaseModel
from typing import Optional
from subjects.dataclasses import Subject
from datetime import datetime


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
