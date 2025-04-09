from bookings.dataclasses import BookingResponse, ProposeBooking, ProposeBookingRequest, UpdateBooking, UpdateBookingRequest
import uuid
from fastapi import HTTPException
from core.db_connection import supabase

def check_if_booking_exists(booking_id: int) -> None | HTTPException:
    booking = supabase.table("bookings").select("*").eq("id", booking_id).execute()
    if not booking.data:
        raise HTTPException(404, 'Booking not found')
    
def update_booking_status(booking_id: int, status: str) -> str:
    supabase.table("bookings").update({"status": status}).eq("id", booking_id).execute()
    return f"Booking {status} successfully"

def update_booking_is_paid(booking_id: int, is_paid: bool) -> str:
    supabase.table("bookings").update({"is_paid": is_paid}).eq("id", booking_id).execute()
    return f"Booking marked as {'paid' if is_paid else 'unpaid'} successfully"

class BookingsService:
    async def get_bookings(self, tutor_id: uuid.UUID) -> list[BookingResponse]:
        bookings_by_tutor = supabase.rpc('get_bookings_by_tutor', {
            'tutor_uuid': str(tutor_id)
        }).execute()

        for booking in bookings_by_tutor.data:
            booking['start_date'] = booking['start_date'].isoformat()
            booking['end_date'] = booking['end_date'].isoformat()
            booking['created_at'] = booking['created_at'].isoformat()
            booking['student_id'] = str(booking['student_id'])

        return bookings_by_tutor.data
    
    async def propose_booking(self, booking_data: ProposeBookingRequest, student_id: uuid.UUID) -> str:
        start_date = booking_data.start_date.isoformat()
        end_date = booking_data.end_date.isoformat()

        if end_date < start_date:
            raise HTTPException(400, 'End date must be greater than start date')
        
        new_booking = ProposeBooking(
            offer_id=booking_data.offer_id, 
            student_id=str(student_id), 
            start_date=start_date,
            end_date=end_date,
            notes=booking_data.notes)
        
        booking = supabase.table("bookings").insert(new_booking.model_dump()).execute()
        if not booking.data:
            raise HTTPException(400, 'Booking proposal failed')
        
        return 'Booking proposed successfully'

    async def update_booking(self, booking_id: int, update_booking_data: UpdateBookingRequest) -> str:
        check_if_booking_exists(booking_id)
        end_date = update_booking_data.end_date.isoformat()
        start_date = update_booking_data.start_date.isoformat()
        if end_date < start_date:
            raise HTTPException(400, 'End date must be greater than start date')
        
        updated_booking = UpdateBooking(
            start_date=start_date,
            end_date=end_date, 
            notes=update_booking_data.notes,
        )
        supabase.table("bookings").update(updated_booking.model_dump()).eq("id", booking_id).execute()
        return 'Booking updated successfully'

    async def accept_booking(self, booking_id: int) -> str:
        check_if_booking_exists(booking_id)
        return update_booking_status(booking_id, "accepted")
    
    async def reject_booking(self, booking_id: int) -> str:
        check_if_booking_exists(booking_id)
        return update_booking_status(booking_id, "rejected")
    
    async def cancel_booking(self, booking_id: int) -> str:
        check_if_booking_exists(booking_id)
        return update_booking_status(booking_id, "canceled")
    
    async def mark_booking_paid(self, booking_id: int) -> str:
        check_if_booking_exists(booking_id)
        return update_booking_is_paid(booking_id, True)

    async def mark_booking_unpaid(self, booking_id: int) -> str:
        check_if_booking_exists(booking_id)
        return update_booking_is_paid(booking_id, False)