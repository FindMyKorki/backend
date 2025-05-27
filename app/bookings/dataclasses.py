from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Annotated
from fastapi import File, UploadFile


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
    price: float

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
    notes: Optional[str] = None
    # left remove_files id's as a string, as fastapi struggles while parsing int input from form
    remove_files: Optional[List[str]] = None

    class Config:
        from_attributes = True


class UpdateBooking(BaseModel):
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class ProposeBookingRequest(BaseModel):
    offer_id: int
    start_date: datetime
    end_date: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class ProposeBooking(ProposeBookingRequest):
    student_id: str
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
