from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class OfferReport(BaseModel):
    id: int
    created_at: datetime
    user_id: str
    offer_id: int
    reason: str
    message: str

    class Config:
        from_attributes = True


class CreateOfferReport(BaseModel):
    reason: str
    message: str

    class Config:
        from_attributes = True
