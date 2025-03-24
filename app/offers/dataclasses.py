from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class offer(BaseModel):
    id: int
    tutor_id: int
    title: str
    description: str
    subject_id: int
    price: float


class offer_level(BaseModel):
    offer_id: int
    level_id: int


class subjects(BaseModel):
    id: int
    subject: str