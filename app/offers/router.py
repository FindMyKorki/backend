from fastapi import APIRouter, Depends, Path, Query
from typing_extensions import Literal
from users.auth import authenticate_user

from .dataclasses import OfferResponse, UpdateOfferRequest, TutorOfferResponse, ActiveOfferResponse
from .service import OffersService, SortBy, Order

offers_router = APIRouter()
offers_service = OffersService()


@offers_router.get("/offers/{offer_id}", response_model=OfferResponse)
async def get_offer(offer_id: int) -> OfferResponse:
    """
    Retrieve a specific offer by its ID

    Args:
        offer_id (int): Unique identifier of the offer

    Returns:
        OfferResponse: Offer details including id, price, description, tutor_avatar_url, tutor_rating, subject_name, icon_url, level
    """
    return await offers_service.get_offer(offer_id)


@offers_router.put("/offers/{offer_id}", response_model=str)
async def update_offer(offer_id: int, request: UpdateOfferRequest) -> str:
    """
    Update the details of an existing offer.

    Args:
        offer_id (int): ID of the offer to be updated.
        request (UpdateOfferRequest): Fields to update in the offer (subject_id, price, description, level_id).

    Returns:
        str: Confirmation message.
    """
    return await offers_service.update_offer(offer_id, request)


@offers_router.post("/offers/{offer_id}:disable", response_model=str)
async def disable_offer(offer_id: int) -> str:
    """
    Disable a specific offer, set `is_active` to False.

    Args:
        offer_id (int): ID of the offer to disable.

    Returns:
        str: Confirmation message.
    """
    return await offers_service.disable_enable_offer(offer_id, False)


@offers_router.post("/offers/{offer_id}:enable", response_model=str)
async def enable_offer(offer_id: int) -> str:
    """
    Enable a specific offer, set `is_active` to True.

    Args:
        offer_id (int): ID of the offer to enable.

    Returns:
        str: Confirmation message.
    """
    return await offers_service.disable_enable_offer(offer_id, True)


@offers_router.get("/tutor-offers/by-tutor/{tutor_id}", response_model=list[TutorOfferResponse])
async def get_tutor_offers(tutor_id: str) -> list[TutorOfferResponse]:
    """
    Retrieve all offers related to a specific tutor.

    Args:
        tutor_id (str): Tutor UUID.

    Returns:
        List[TutorOfferResponse]: List of offers related to the tutor.
    """
    return await offers_service.get_tutor_offers(tutor_id)


@offers_router.get("/tutor-offers/by-id/{offer_id}", response_model=TutorOfferResponse)
async def get_tutor_offer(offer_id: int) -> TutorOfferResponse:
    """
    Retrieve a detailed tutor offer by offer ID.

    Args:
        offer_id (int): ID of the offer.

    Returns:
        TutorOfferResponse: Detailed information about the tutor's offer.
    """
    return await offers_service.get_tutor_offer(offer_id)


@offers_router.get("/active-offers/{tutor_id}", response_model=list[TutorOfferResponse])
async def get_tutor_active_offer(tutor_id: str) -> list[TutorOfferResponse]:
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
        sort_by: SortBy = Query(...),
        order: Order = Query(...)
) -> list[TutorOfferResponse]:
    """
    Retrieve a list of all active offers in the system, with sorting options.

    Query Parameters:
        sort_by (SortBy): Field to sort offers by rating, price or name.
        order (Order): Sorting order increasing or decreasing.

    Returns:
        List[ActiveOfferResponse]: Sorted list of active tutor offers.
    """
    return await offers_service.get_active_offers(sort_by, order)
