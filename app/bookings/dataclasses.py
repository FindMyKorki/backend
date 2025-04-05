from pydantic import BaseModel


class UpsertBooking(BaseModel):
    offer_id: int
    student_id: str | None = None
    start_date: str              # not a datetime, because supabase doesn't support it
    end_date: str                #
    status: str
    notes: str | None = None
    is_paid: bool

    class Config:
        from_attributes = True


class Booking(UpsertBooking):
    id: int
    created_at: str

