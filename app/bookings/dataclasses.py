from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Booking(BaseModel):
    id: int
    created_at: datetime
    user_id: int
    offer_id: int
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class CreateBooking(BaseModel):
    user_id: int
    offer_id: int
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None
    status: BookingStatus = BookingStatus.PENDING

    class Config:
        from_attributes = True


class UpdateBooking(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[BookingStatus] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True