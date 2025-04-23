from pydantic import BaseModel


class UpsertBookingAttachment(BaseModel):
    booking_id: int
    attachment_url: str

    class Config:
        from_attributes = True


class BookingAttachment(UpsertBookingAttachment):
    id: int
    created_at: str
