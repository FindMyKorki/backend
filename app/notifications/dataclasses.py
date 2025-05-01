from pydantic import BaseModel


class UpsertBooking(BaseModel):
    user_id: str
    title: str
    message: str
    type: str

    class Config:
        from_attributes = True


class Booking(UpsertBooking):
    id: int
    created_at: str
