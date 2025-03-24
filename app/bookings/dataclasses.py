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
    id: str  # uuid
    created_at: datetime
    user_id: str  # uuid
    offer_id: str  # uuid
    start_date: datetime  # Changed from start_time
    end_date: datetime  # Changed from end_time
    status: BookingStatus
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class CreateBooking(BaseModel):
    user_id: str  # uuid
    offer_id: str  # uuid
    start_date: datetime  # Changed from start_time
    end_date: datetime  # Changed from end_time
    notes: Optional[str] = None
    status: BookingStatus = BookingStatus.PENDING

    class Config:
        from_attributes = True


class UpdateBooking(BaseModel):
    start_date: Optional[datetime] = None  # Changed from start_time
    end_date: Optional[datetime] = None  # Changed from end_time
    status: Optional[BookingStatus] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True