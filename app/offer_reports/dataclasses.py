from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CreateOfferReport(BaseModel):
    message: Optional[str] = ""

    class Config:
        from_attributes = True


class OfferReport(CreateOfferReport):
    id: int
    reason: str
    created_at: datetime
    user_id: str
    offer_id: int

    class Config:
        from_attributes = True
