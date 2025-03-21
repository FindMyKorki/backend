from bookings.dataclasses import Booking, CreateBooking, UpdateBooking, BookingStatus
from core.db_connection import supabase
from datetime import datetime


class BookingsService:
    async def get_bookings(self, status: BookingStatus = None) -> list[Booking]:
        query = supabase.table("bookings").select("*")

        if status:
            query = query.eq("status", status)

        bookings = query.execute()
        return bookings.data

    async def get_booking(self, booking_id: int) -> Booking:
        booking = (
            supabase.table("bookings")
            .select("*")
            .eq("id", booking_id)
            .execute()
        )
        return booking.data[0] if booking.data else None

    async def get_user_bookings(self, user_id: int, status: BookingStatus = None) -> list[Booking]:
        query = (
            supabase.table("bookings")
            .select("*")
            .eq("user_id", user_id)
        )

        if status:
            query = query.eq("status", status)

        bookings = query.execute()
        return bookings.data

    async def get_offer_bookings(self, offer_id: int, status: BookingStatus = None) -> list[Booking]:
        query = (
            supabase.table("bookings")
            .select("*")
            .eq("offer_id", offer_id)
        )

        if status:
            query = query.eq("status", status)

        bookings = query.execute()
        return bookings.data

    async def create_booking(self, create_booking_data: CreateBooking) -> str:
        new_booking = (
            supabase.table("bookings")
            .insert(create_booking_data.model_dump())
            .execute()
        )

        booking_id = new_booking.data[0].get("id")

        return f"Created new booking with id {booking_id}"

    async def update_booking(self, booking_id: int, update_data: UpdateBooking) -> str:
        # Filter out None values
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

        if not update_dict:
            return "No fields to update"

        updated_booking = (
            supabase.table("bookings")
            .update(update_dict)
            .eq("id", booking_id)
            .execute()
        )

        return f"Updated booking with id {booking_id}"

    async def cancel_booking(self, booking_id: int) -> str:
        cancelled_booking = (
            supabase.table("bookings")
            .update({"status": BookingStatus.CANCELLED})
            .eq("id", booking_id)
            .execute()
        )

        return f"Cancelled booking with id {booking_id}"

    async def delete_booking(self, booking_id: int) -> str:
        deleted_booking = (
            supabase.table("bookings")
            .delete()
            .eq("id", booking_id)
            .execute()
        )

        return f"Deleted booking with id {booking_id}"