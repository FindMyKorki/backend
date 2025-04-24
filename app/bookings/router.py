from bookings.dataclasses import TutorBookingResponse, UpdateBookingRequest, ProposeBookingRequest, \
    StudentBookingResponse
from bookings.service import BookingsService
from fastapi import APIRouter, Depends, Path
from gotrue.types import UserResponse
from users.auth import authenticate_user

bookings_router = APIRouter()
bookings_service = BookingsService()


@bookings_router.get("/tutor/bookings", response_model=list[TutorBookingResponse])
async def get_bookings(_user_response: UserResponse = Depends(authenticate_user)):
    """
    Retrieve all bookings associated with a specific tutor.

    Args:
        _user_response (UserResponse): The user details from the authentication service.

    Returns:
        list[TutorBookingResponse]: A list of bookings for the tutor, containing booking details.
    """
    return await bookings_service.get_bookings_by_tutor(tutor_id=_user_response.user.id)


@bookings_router.get("/student/bookings", response_model=list[StudentBookingResponse])
async def get_bookings(_user_response: UserResponse = Depends(authenticate_user)):
    """
    Retrieve all bookings associated with a specific student.

    Args:
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        list[StudentBookingResponse]: A list of bookings for the student, containing booking details.
    """
    return await bookings_service.get_bookings_by_student(student_id=_user_response.user.id)


@bookings_router.put("/bookings/{booking_id}", response_model=str)
async def update_booking(booking_data: UpdateBookingRequest,
                         booking_id: int = Path(...),
                         _user_response: UserResponse = Depends(authenticate_user)):
    """
    Update the details of an existing booking.

    Args:
        booking_data (UpdateBookingRequest): The new data to update the booking with (start_date, end_date, notes, etc.).
        booking_id (int): The unique identifier of the booking to be updated.
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        str: A confirmation message indicating the booking was successfully updated.
    """
    return await bookings_service.update_booking(booking_id, _user_response.user.id, booking_data)


@bookings_router.post("/bookings:propose", response_model=str)
async def propose_booking(propose_booking_data: ProposeBookingRequest,
                          _user_response: UserResponse = Depends(authenticate_user)):
    """
    Propose a new booking for a student.

    Args:
        propose_booking_data (ProposeBookingRequest): The details of the proposed booking (dates, tutor ID, etc.).
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        str: A confirmation message or the ID of the proposed booking.
    """
    return await bookings_service.propose_booking(booking_data=propose_booking_data, student_id=_user_response.user.id)


@bookings_router.post("/bookings/{booking_id}:accept", response_model=str)
async def accept_booking(booking_id: int = Path(...), _user_response: UserResponse = Depends(authenticate_user)):
    """
    Accept a booking request as a tutor.

    Args:
        booking_id (int): The unique identifier of the booking to be accepted.
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        str: A confirmation message indicating the booking was accepted.
    """
    return await bookings_service.accept_booking(booking_id, _user_response.user.id)


@bookings_router.post("/bookings/{booking_id}:reject", response_model=str)
async def reject_booking(booking_id: int = Path(...), _user_response: UserResponse = Depends(authenticate_user)):
    """
    Reject a booking request as a tutor.

    Args:
        booking_id (int): The unique identifier of the booking to be rejected.
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        str: A confirmation message indicating the booking was rejected.
    """
    return await bookings_service.reject_booking(booking_id, _user_response.user.id)


@bookings_router.post("/bookings/{booking_id}:cancel", response_model=str)
async def cancel_booking(booking_id: int = Path(...), _user_response: UserResponse = Depends(authenticate_user)):
    """
    Cancel an existing booking as either the student or the tutor.

    Args:
        booking_id (int): The unique identifier of the booking to be canceled.
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        str: A confirmation message indicating the booking was canceled.
    """
    return await bookings_service.cancel_booking(booking_id, _user_response.user.id)


@bookings_router.post("/bookings/{booking_id}:mark-paid", response_model=str)
async def mark_booking_as_paid(booking_id: int = Path(...), _user_response: UserResponse = Depends(authenticate_user)):
    """
    Mark a booking as paid by the tutor.

    Args:
        booking_id (int): The unique identifier of the booking to be marked as paid.
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        str: A confirmation message indicating the booking was marked as paid.
    """
    return await bookings_service.mark_booking_paid(booking_id, _user_response.user.id)


@bookings_router.post("/bookings/{booking_id}:mark-unpaid", response_model=str)
async def mark_booking_as_unpaid(booking_id: int = Path(...), _user_response: UserResponse = Depends(authenticate_user)):
    """
    Mark a booking as unpaid by the tutor.

    Args:
        booking_id (int): The unique identifier of the booking to be marked as unpaid.
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        str: A confirmation message indicating the booking was marked as unpaid.
    """
    return await bookings_service.mark_booking_unpaid(booking_id, _user_response.user.id)
