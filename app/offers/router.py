from enum import Enum
from fastapi import APIRouter, Depends, Path, Query
from typing_extensions import Literal
from users.auth import authenticate_user

from .dataclasses import OfferResponse, UpdateOfferRequest, TutorOfferResponse, ActiveOfferResponse
from .service import OffersService

offers_router = APIRouter()
offers_service = OffersService()


class SortBy(str, Enum):
    rating = "rating"
    price = "price"
    reviews = "reviews"


class Order(str, Enum):
    increasing = "increasing"
    decreasing = "decreasing"


@offers_router.get("/offers/{offer_id}", response_model=OfferResponse)
async def get_offer(offer_id: int):
    return await offers_service.get_offer(offer_id)


@offers_router.put("/offers/{offer_id}", response_model=int)
async def update_offer(offer_id: int, request: UpdateOfferRequest):
    return await offers_service.update_offer(offer_id, request)


@offers_router.post("/offers/{offer_id}:disable")
async def disable_offer(offer_id: int):
    return await offers_service.disable_enable_offer(offer_id, False)


@offers_router.post("/offers/{offer_id}:enable")
async def enable_offer(offer_id: int):
    return await offers_service.disable_enable_offer(offer_id, True)


@offers_router.get("/tutor-offers/by-tutor/{tutor_id}")
async def get_tutor_offers(tutor_id: str) -> list[TutorOfferResponse]:
    return await offers_service.get_tutor_offers(tutor_id)


@offers_router.get("/tutor-offers/by-id/{offer_id}")
async def get_tutor_offer(offer_id: int) -> TutorOfferResponse:
    return await offers_service.get_tutor_offer(offer_id)


@offers_router.get("/active-offers/{tutor_id}", response_model=list[TutorOfferResponse])
async def get_tutor_active_offer(tutor_id: str) -> list[TutorOfferResponse]:
    return await offers_service.get_tutor_active_offer(tutor_id)


@offers_router.get("/active-offers", response_model=list[ActiveOfferResponse])
async def get_active_offers(
        sort_by: SortBy = Query(...),
        order: Order = Query(...)
) -> list[TutorOfferResponse]:
    return await offers_service.get_active_offers(sort_by, order)
