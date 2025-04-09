from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel

class Booking(BaseModel):
    id: int
    offer_id: int
    student_id: uuid.UUID
    status: str # "pending", "accepted", "canceled", "rejected"
    start_date: datetime
    end_date: datetime
    created_at: datetime
    is_paid: bool
    notes: Optional[str]

    class Config:
        from_attributes = True

class BookingResponse(BaseModel):
    id: int
    subject: str
    student_id: uuid.UUID
    student_full_name: str
    avatar_url: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    status: str
    is_paid: bool
    notes: Optional[str]

    class Config:
        from_attributes = True

class ProposeBookingRequest(BaseModel):
    offer_id: int
    start_date: datetime
    end_date: datetime
    notes: Optional[str]

    class Config:
        from_attributes = True

class ProposeBooking(BaseModel):
    offer_id: int
    student_id: str
    start_date: str
    end_date: str
    notes: Optional[str]
    status: str = 'pending'
    is_paid: bool = False
    created_at: str = datetime.now().isoformat()

    class Config:
        from_attributes = True

class UpdateBookingRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    notes: Optional[str]

    class Config:
        from_attributes = True

class UpdateBooking(BaseModel):
    start_date: str
    end_date: str
    notes: Optional[str]

    class Config:
        from_attributes = True

class BookingCancelRequest(BaseModel):
    canceled_by: int

    class Config:
        from_attributes = True