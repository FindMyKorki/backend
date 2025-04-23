from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Booking(BaseModel):
    id: int
    offer_id: int
    student_id: Optional[str]
    status: str  # "pending", "accepted", "canceled", "rejected"
    start_date: datetime
    end_date: datetime
    created_at: datetime
    is_paid: bool
    notes: Optional[str]

    class Config:
        from_attributes = True


class TutorBookingResponse(BaseModel):
    id: int
    subject: str
    student_id: str
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


class StudentBookingResponse(BaseModel):
    id: int
    subject: str
    tutor_id: str
    tutor_full_name: str
    avatar_url: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    status: str
    is_paid: bool
    price: float
    notes: Optional[str]

    class Config:
        from_attributes = True


class ProposeBookingRequest(BaseModel):
    offer_id: int
    start_date: datetime
    end_date: datetime
    notes: Optional[str] = ""

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


# Crud
class UpsertBooking(BaseModel):
    offer_id: int
    student_id: Optional[str]
    start_date: str  # not a datetime, because supabase doesn't support it
    end_date: str  #
    status: str
    notes: Optional[str]
    is_paid: bool = False

    class Config:
        from_attributes = True
