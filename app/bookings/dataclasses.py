import datetime
from pydantic import BaseModel

class Booking(BaseModel):
    id: int
    offer_id: int
    student_id: int
    status: str # "pending", "accepted", "canceled", "rejected"
    notes: str
    start_time: datetime
    end_time: datetime
    created_at: datetime
    is_paid: bool

    class Config:
        from_attributes = True

class BookingResponse(BaseModel):
    id: int
    subject: str
    student_id: int
    student_full_name: str
    start_date: datetime
    end_date: datetime
    notes: str
    created_at: datetime
    status: str
    is_paid: bool

    class Config:
        from_attributes = True

class ProposeBookingRequest(BaseModel):
    offer_id: int
    student_id: int
    notes: str
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True

class UpdateBookingRequest(BaseModel):
    notes: str
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True

class BookingCancelRequest(BaseModel):
    canceled_by: int

    class Config:
        from_attributes = True