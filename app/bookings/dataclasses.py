from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Booking(BaseModel):
    id: int
    offer_id: int
    student_id: str
    status: str  # "pending", "accepted", "canceled", "rejected"
    start_date: datetime
    end_date: datetime
    created_at: datetime
    is_paid: bool
    notes: Optional[str]

    class Config:
        from_attributes = True


class TutorBookingResponse(Booking):
    subject_name: str
    subject_icon_url: Optional[str]
    student_full_name: str
    avatar_url: str

    class Config:
        from_attributes = True


class StudentBookingResponse(Booking):
    subject_name: str
    subject_icon_url: Optional[str]
    tutor_id: str
    tutor_full_name: str
    avatar_url: str
    price: float

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


class ProposeBookingRequest(UpdateBookingRequest):
    offer_id: int

    class Config:
        from_attributes = True


class ProposeBooking(ProposeBookingRequest):
    student_id: str
    start_date: str
    end_date: str
    status: str = 'pending'
    is_paid: bool = False

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
