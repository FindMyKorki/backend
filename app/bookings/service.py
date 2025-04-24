from core.db_connection import supabase
from crud.crud_provider import CRUDProvider
from fastapi import HTTPException

from .dataclasses import Booking, UpsertBooking, TutorBookingResponse, StudentBookingResponse, ProposeBooking, \
    ProposeBookingRequest, UpdateBooking, UpdateBookingRequest

crud_provider = CRUDProvider("bookings")


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
    async def get_bookings_by_tutor(self, tutor_id: str) -> list[TutorBookingResponse]:
        bookings_by_tutor = supabase.rpc('get_bookings_by_tutor_fix', {
            'tutor_uuid': str(tutor_id)
        }).execute()

        return bookings_by_tutor.data

    async def get_bookings_by_student(self, student_id: str) -> list[StudentBookingResponse]:
        bookings_by_student = supabase.rpc('get_bookings_by_student_fix', {
            'student_uuid': str(student_id)
        }).execute()

        return bookings_by_student.data

    async def propose_booking(self, booking_data: ProposeBookingRequest, student_id: str) -> str:
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
        # TODO: check if user requesting update is either student or tutor related to that booking

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
        # TODO: check if user accepting booking is the tutor related to that booking
        return update_booking_status(booking_id, "accepted")

    async def reject_booking(self, booking_id: int) -> str:
        check_if_booking_exists(booking_id)
        # TODO: check if user rejecting booking is the tutor related to that booking
        return update_booking_status(booking_id, "rejected")

    async def cancel_booking(self, booking_id: int) -> str:
        check_if_booking_exists(booking_id)
        # TODO: check if user cancelling booking is either tutor or student related to that booking
        return update_booking_status(booking_id, "canceled")

    async def mark_booking_paid(self, booking_id: int) -> str:
        check_if_booking_exists(booking_id)
        # TODO: check if user marking booking as paid is the tutor related to that booking
        return update_booking_is_paid(booking_id, True)

    async def mark_booking_unpaid(self, booking_id: int) -> str:
        check_if_booking_exists(booking_id)
        # TODO: check if user marking booking as unpaid is the tutor related to that booking
        return update_booking_is_paid(booking_id, False)

    # CRUD
    async def create_booking(self, booking: UpsertBooking, id: int = None) -> Booking:
        new_booking = await crud_provider.create(booking.model_dump(exclude="created_at"), id)

        return Booking.model_validate(new_booking)

    async def get_booking(self, id: int) -> Booking:
        booking = await crud_provider.get(id)

        return Booking.model_validate(booking)

    async def update_booking2(self, booking: UpsertBooking, id: int = None) -> Booking:
        updated_booking = await crud_provider.update(booking.model_dump(exclude="created_at"), id)

        return Booking.model_validate(updated_booking)

    async def delete_booking(self, id: int) -> Booking:
        deleted_booking = await crud_provider.delete(id)

        return Booking.model_validate(deleted_booking)
