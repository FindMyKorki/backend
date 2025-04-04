from crud.crud_provider import CRUDProvider
from .dataclasses import Booking, UpsertBooking


crud_provider = CRUDProvider("bookings")


class BookingService:
    async def create_booking(self, booking: UpsertBooking, id: int = None) -> Booking:
        new_booking = await crud_provider.create(booking.model_dump(), id)

        return Booking.model_validate(new_booking)

    async def get_booking(self, id: int) -> Booking:
        booking = await crud_provider.get(id)

        return Booking.model_validate(booking)

    async def update_booking(self, booking: UpsertBooking, id: int = None) -> Booking:
        updated_booking = await crud_provider.update(booking.model_dump(), id)

        return Booking.model_validate(updated_booking)

    async def delete_booking(self, id: int) -> Booking:
        deleted_booking = await crud_provider.delete(id)

        return Booking.model_validate(deleted_booking)

