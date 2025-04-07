from pydantic import BaseModel
from typing import Optional
from subjects.dataclasses import Subject
from datetime import datetime


class Level(BaseModel):
    id: int
    level: str

    class Config:
        from_attributes = True


class Offer(BaseModel):
    id: int
    tutor_id: str
    price: Optional[float]
    subject: Optional[Subject]
    title: Optional[str]
    description: Optional[str]
    is_active: bool
    created_at: datetime
    level: Optional[Level]

    class Config:
        from_attributes = True


class CreateOffer(BaseModel):
    price: Optional[float]
    subject_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    is_active: bool
    level_id: Optional[int]

    class Config:
        from_attributes = True


class UpdateOffer(BaseModel):
    id: int
    price: Optional[float]
    subject_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    is_active: bool
    level_id: Optional[int]

    class Config:
        from_attributes = True
