from offers.service import OffersService
from offers.dataclasses import Offer, CreateOffer, UpdateOffer

from fastapi import APIRouter, HTTPException, Path, Query

offers_router = APIRouter()
offers_service = OffersService()


@offers_router.get("/offers", response_model=list[Offer])
async def get_offers(active_only: bool = Query(False, description="Filter to show only active offers")):
    return await offers_service.get_offers(active_only)


@offers_router.get("/offer/{offer_id}", response_model=Offer)
async def get_offer(offer_id: int = Path(..., title="The ID of the offer")):
    offer = await offers_service.get_offer(offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer


@offers_router.get("/tutor/{tutor_profile_id}/offers", response_model=list[Offer])
async def get_tutor_offers(
        tutor_profile_id: int = Path(..., title="The ID of the tutor profile"),
        active_only: bool = Query(False, description="Filter to show only active offers")
):
    return await offers_service.get_tutor_offers(tutor_profile_id, active_only)


@offers_router.post("/offer", response_model=str)
async def create_offer(create_offer_data: CreateOffer):
    return await offers_service.create_offer(create_offer_data)


@offers_router.put("/offer/{offer_id}", response_model=str)
async def update_offer(
        update_data: UpdateOffer,
        offer_id: int = Path(..., title="The ID of the offer to update")
):
    # Check if offer exists
    offer = await offers_service.get_offer(offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    return await offers_service.update_offer(offer_id, update_data)


@offers_router.delete("/offer/{offer_id}", response_model=str)
async def delete_offer(offer_id: int = Path(..., title="The ID of the offer to delete")):
    # Check if offer exists
    offer = await offers_service.get_offer(offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    return await offers_service.delete_offer(offer_id)