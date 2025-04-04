from bookings.service import BookingsService
# from bookings.dataclasses import Level, CreateLevelRequest

from fastapi import APIRouter

bookings_router = APIRouter()
bookings_service = BookingsService()

# @bookings_router.get("/bookings", response_model=list[Level])
# async def get_levels():
#     return await levels_service.get_levels()

# @bookings_router.post("/levels", response_model=str)
# async def create_level(create_level_data: CreateLevelRequest):
#     return await levels_service.create_level(create_level_data)

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