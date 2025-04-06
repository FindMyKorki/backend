from bookings.dataclasses import BookingResponse, ProposeBooking, ProposeBookingRequest, UpdateBooking, UpdateBookingRequest
import uuid
from fastapi import HTTPException
from bookings.dataclasses import BookingResponse
from core.db_connection import supabase

def check_is_booking_exists(booking_id: int) -> None | HTTPException:
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
        offers_by_tutor = supabase.table("offers").select("*").eq("tutor_id", tutor_id).execute()

        if not offers_by_tutor.data:
            raise HTTPException(404, 'No bookings found')
        
        bookings_by_tutor = []

        for offer in offers_by_tutor.data:
            bookings = supabase.table("bookings").select("*").eq("offer_id", offer["id"]).execute()

            if not bookings.data:
                raise HTTPException(404, 'No bookings found')
            
            for booking in bookings.data:
                b_subject = supabase.table("subjects").select("name").eq("id", offer["subject_id"]).execute().data[0]["name"]
                b_student_full_name = supabase.table("profiles").select("full_name").eq("id", booking["student_id"]).execute().data[0]["full_name"]
                booking = BookingResponse(**booking, subject=b_subject, student_full_name=b_student_full_name)

                bookings_by_tutor.append(booking)

        return bookings_by_tutor
    
    async def propose_booking(self, booking_data: ProposeBookingRequest) -> str:
        start_date = booking_data.start_date.isoformat()
        end_date = booking_data.end_date.isoformat()

        if end_date < start_date:
            raise HTTPException(400, 'End date must be greater than start date')
        
        new_booking = ProposeBooking(
            offer_id=booking_data.offer_id, 
            student_id=str(booking_data.student_id), 
            start_date=start_date,
            end_date=end_date,
            notes=booking_data.notes)
        
        booking = supabase.table("bookings").insert(new_booking.model_dump()).execute()
        if not booking.data:
            raise HTTPException(400, 'Booking proposal failed')
        
        return 'Booking proposed successfully'

    async def update_booking(self, booking_id: int, update_booking_data: UpdateBookingRequest) -> str:
        check_is_booking_exists(booking_id)
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
        check_is_booking_exists(booking_id)
        return update_booking_status(booking_id, "accepted")
    
    async def reject_booking(self, booking_id: int) -> str:
        check_is_booking_exists(booking_id)
        return update_booking_status(booking_id, "rejected")
    
    async def cancel_booking(self, booking_id: int) -> str:
        check_is_booking_exists(booking_id)
        return update_booking_status(booking_id, "canceled")
    
    async def mark_booking_paid(self, booking_id: int) -> str:
        check_is_booking_exists(booking_id)
        return update_booking_is_paid(booking_id, True)

    async def mark_booking_unpaid(self, booking_id: int) -> str:
        check_is_booking_exists(booking_id)
        return update_booking_is_paid(booking_id, False)