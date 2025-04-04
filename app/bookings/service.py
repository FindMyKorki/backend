# from bookings.dataclasses import BookingCancelRequest, BookingResponse, ProposeBookingRequest, UpdateBookingRequest
from fastapi import HTTPException
from core.db_connection import supabase

def check_is_booking_exists(booking_id: int) -> None | HTTPException:
    booking = supabase.table("bookings").select("*").eq("id", booking_id).execute()
    if not booking.data:
        raise HTTPException(404, 'Booking not found')
    
def update_booking_status(booking_id: int, status: str) -> None:
    supabase.table("bookings").update({"status": status}).eq("id", booking_id).execute()
    raise HTTPException(200, f"Booking {status} successfully")

def update_booking_is_paid(booking_id: int, is_paid: bool) -> None:
    supabase.table("bookings").update({"is_paid": is_paid}).eq("id", booking_id).execute()
    raise HTTPException(200, f"Booking marked as {'paid' if is_paid else 'unpaid'} successfully")

class BookingsService:
    async def accept_booking(self, booking_id: int) -> str:
        check_is_booking_exists(booking_id)
        update_booking_status(booking_id, "accepted")
    
    async def reject_booking(self, booking_id: int) -> str:
        check_is_booking_exists(booking_id)
        update_booking_status(booking_id, "rejected")
    
    async def cancel_booking(self, booking_id: int) -> str:
        check_is_booking_exists(booking_id)
        update_booking_status(booking_id, "canceled")
    
    async def mark_booking_paid(self, booking_id: int) -> str:
        check_is_booking_exists(booking_id)
        update_booking_is_paid(booking_id, True)

    async def mark_booking_unpaid(self, booking_id: int) -> str:
        check_is_booking_exists(booking_id)
        update_booking_is_paid(booking_id, False)