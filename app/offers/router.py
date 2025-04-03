from fastapi import APIRouter, Depends, Path
from users.auth import authenticate_user


from .dataclasses import OfferResponse, UpdateOfferRequest, TutorOfferResponse
from .service import OffersService

offers_router = APIRouter()
offers_service = OffersService()


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


# GET /active-offers/{tutor_id}
# GET /active-offers?sort_by=&order=
