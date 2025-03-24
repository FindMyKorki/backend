from bookings.service import BookingsService
from bookings.dataclasses import Booking, CreateBooking, UpdateBooking, BookingStatus

from fastapi import APIRouter, HTTPException, Path, Query
from typing import Optional

bookings_router = APIRouter()
bookings_service = BookingsService()


@bookings_router.get("/bookings", response_model=list[Booking])
async def get_bookings(status: Optional[BookingStatus] = Query(None, description="Filter by booking status")):
    return await bookings_service.get_bookings(status)


@bookings_router.get("/booking/{booking_id}", response_model=Booking)
async def get_booking(booking_id: int = Path(..., title="The ID of the booking")):
    booking = await bookings_service.get_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@bookings_router.get("/user/{user_id}/bookings", response_model=list[Booking])
async def get_user_bookings(
        user_id: int = Path(..., title="The ID of the user"),
        status: Optional[BookingStatus] = Query(None, description="Filter by booking status")
):
    return await bookings_service.get_user_bookings(user_id, status)


@bookings_router.get("/offer/{offer_id}/bookings", response_model=list[Booking])
async def get_offer_bookings(
        offer_id: int = Path(..., title="The ID of the offer"),
        status: Optional[BookingStatus] = Query(None, description="Filter by booking status")
):
    return await bookings_service.get_offer_bookings(offer_id, status)


@bookings_router.post("/booking", response_model=str)
async def create_booking(create_booking_data: CreateBooking):
    return await bookings_service.create_booking(create_booking_data)


@bookings_router.put("/booking/{booking_id}", response_model=str)
async def update_booking(
        update_data: UpdateBooking,
        booking_id: int = Path(..., title="The ID of the booking to update")
):
    # Check if booking exists
    booking = await bookings_service.get_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return await bookings_service.update_booking(booking_id, update_data)


@bookings_router.patch("/booking/{booking_id}/cancel", response_model=str)
async def cancel_booking(booking_id: int = Path(..., title="The ID of the booking to cancel")):
    # Check if booking exists
    booking = await bookings_service.get_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status == BookingStatus.CANCELLED:
        return f"Booking {booking_id} is already cancelled"

    return await bookings_service.cancel_booking(booking_id)


@bookings_router.delete("/booking/{booking_id}", response_model=str)
async def delete_booking(booking_id: int = Path(..., title="The ID of the booking to delete")):
    # Check if booking exists
    booking = await bookings_service.get_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return await bookings_service.delete_booking(booking_id)