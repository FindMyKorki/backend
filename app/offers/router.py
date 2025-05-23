from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Path, Query
from gotrue.types import UserResponse
from typing_extensions import Literal
from users.auth import authenticate_user

from .dataclasses import OfferResponse, UpdateOfferRequest, TutorOfferResponse, ActiveOfferResponse
from .service import OffersService, Order

offers_router = APIRouter()
offers_service = OffersService()


@offers_router.get("/offers/{offer_id}", response_model=OfferResponse)
async def get_offer(offer_id: int = Path(...)) ->   OfferResponse:
    """
    Retrieve a specific offer by its ID

    Args:
        offer_id (int): Unique identifier of the offer

    Returns:
        OfferResponse: Offer details including id, tutor_id, price, description, tutor_avatar_url, tutor_rating, subject_name, icon_url, level
    """
    return await offers_service.get_offer(offer_id)


@offers_router.put("/offers/{offer_id}", response_model=str)
async def update_offer(request: UpdateOfferRequest, offer_id: int = Path(...),
                       _user_response: UserResponse = Depends(authenticate_user)) -> str:
    """
    Update the details of an existing offer.

    Args:
        offer_id (int): ID of the offer to be updated.
        request (UpdateOfferRequest): Fields to update in the offer (subject_id, price, description, level_id).
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        str: Confirmation message.
    """
    return await offers_service.update_offer(offer_id, request, _user_response.user.id)


@offers_router.post("/offers/{offer_id}:disable", response_model=str)
async def disable_offer(offer_id: int = Path(...), _user_response: UserResponse = Depends(authenticate_user)) -> str:
    """
    Disable a specific offer, set `is_active` to False.

    Args:
        offer_id (int): ID of the offer to disable.
        _user_response (UserResponse): The currently authenticated user.


    Returns:
        str: Confirmation message.
    """
    return await offers_service.disable_enable_offer(offer_id, False, _user_response.user.id)


@offers_router.post("/offers/{offer_id}:enable", response_model=str)
async def enable_offer(offer_id: int = Path(...), _user_response: UserResponse = Depends(authenticate_user)) -> str:
    """
    Enable a specific offer, set `is_active` to True.

    Args:
        offer_id (int): ID of the offer to enable.
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        str: Confirmation message.
    """
    return await offers_service.disable_enable_offer(offer_id, True, _user_response.user.id)


@offers_router.get("/tutor-offers/by-tutor", response_model=list[TutorOfferResponse])
async def get_tutor_offers(_user_response: UserResponse = Depends(authenticate_user)) -> list[TutorOfferResponse]:
    """
    Retrieve all offers related to a specific tutor.

    Args:
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        List[TutorOfferResponse]: List of offers related to the tutor.
    """
    return await offers_service.get_tutor_offers(_user_response.user.id)


@offers_router.get("/tutor-offers/by-id/{offer_id}", response_model=TutorOfferResponse)
async def get_tutor_offer(offer_id: int = Path(...),
                          _user_response: UserResponse = Depends(authenticate_user)) -> TutorOfferResponse:
    """
    Retrieve a detailed tutor offer by offer ID.

    Args:
        offer_id (int): ID of the offer.
        _user_response (UserResponse): The currently authenticated user.

    Returns:
        TutorOfferResponse: Detailed information about the tutor's offer.
    """
    return await offers_service.get_tutor_offer(offer_id, _user_response.user.id)


@offers_router.get("/active-offers/{tutor_id}", response_model=list[TutorOfferResponse])
async def get_tutor_active_offer(tutor_id: str = Path(...)) -> list[TutorOfferResponse]:
    """
    Get a list of active offers for a specific tutor.

    Args:
        tutor_id (str): Tutor UUID.

    Returns:
        List[TutorOfferResponse]: List od all currently enabled (active) offers of the tutor.
    """
    return await offers_service.get_tutor_active_offer(tutor_id)


@offers_router.get("/active-offers", response_model=list[ActiveOfferResponse])
async def get_active_offers(
        level_id: int,
        subject_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        order: Optional[Order] = 'ASC',
        limit: Optional[int] = 5,
        offset: Optional[int] = 0
) -> list[TutorOfferResponse]:
    """
    Retrieve a list of all active offers in the system, with sorting options.

    Args:
        level_id - id of selected level (required)
        subject_id - id of selected subject (required)
        start_date, end_date - together they form a date frame for which you want tutor to be available at (optional)
        min_price, max_price - optional
        order - order direction for offers price, either ASC or DESC
    Returns:
        List[ActiveOfferResponse]: Sorted list of active tutor offers.
    """
    return await offers_service.get_active_offers(level_id, subject_id, start_date, end_date, min_price, max_price, order, limit, offset)
