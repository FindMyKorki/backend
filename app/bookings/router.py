from users.auth import authenticate_user
from bookings.service import BookingsService
from bookings.dataclasses import BookingResponse, UpdateBookingRequest, ProposeBookingRequest

from fastapi import APIRouter, Depends

bookings_router = APIRouter()
bookings_service = BookingsService()

@bookings_router.get("/bookings", response_model=list[BookingResponse])
async def get_bookings(user_response=Depends(authenticate_user)):
    return await bookings_service.get_bookings(tutor_id=user_response.user.id)

@bookings_router.put("/bookings/{booking_id}", response_model=str)
async def update_booking(booking_id: int, booking_data: UpdateBookingRequest):
    return await bookings_service.update_booking(booking_id, booking_data)

@bookings_router.post("/bookings:propose", response_model=str)
async def propose_booking(propose_booking_data: ProposeBookingRequest, user_response=Depends(authenticate_user)):
    return await bookings_service.propose_booking(booking_data=propose_booking_data, student_id=user_response.user.id)

@bookings_router.post("/bookings/{booking_id}:accept", response_model=str)
async def accept_booking(booking_id: int):
    return await bookings_service.accept_booking(booking_id)

@bookings_router.post("/bookings/{booking_id}:reject", response_model=str)
async def reject_booking(booking_id: int):
    return await bookings_service.reject_booking(booking_id)

@bookings_router.post("/bookings/{booking_id}:cancel", response_model=str)
async def cancel_booking(booking_id: int):
    return await bookings_service.cancel_booking(booking_id)

@bookings_router.post("/bookings/{booking_id}:mark-paid", response_model=str)
async def mark_booking_as_paid(booking_id: int):
    return await bookings_service.mark_booking_paid(booking_id)

@bookings_router.post("/bookings/{booking_id}:mark-unpaid", response_model=str)
async def mark_booking_as_unpaid(booking_id: int):
    return await bookings_service.mark_booking_unpaid(booking_id)