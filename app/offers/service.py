from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import OfferResponse, UpdateOfferRequest
from .utils import flatten_offer_data


class OffersService:
    async def get_offer(self, offer_id: int) -> OfferResponse:
        response = (
            supabase
            .table("offers")
            .select(
                "id, description, price, "
                "tutor_profiles(id, rating, profiles(full_name)), "
                "subjects(name:subject_name, icon_url), "
                "levels(level)"
            )
            .eq("id", offer_id)
            .single()
            .execute()
        )
        print(response.data)

        if response.data is None:
            raise HTTPException(status_code=404, detail="Offer not found")

        return flatten_offer_data(response.data)

    async def update_offer(self, offer_id: int, request: UpdateOfferRequest) -> int:
        service = OffersService()
        offer = await service.get_offer(offer_id)

        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")
        update_offer = (
            supabase
            .table("offers")
            .update({
                "subject_id": request.subject_id,
                "price": request.price,
                "description": request.description,
                "level_id": request.level_id})
            .eq("id", offer_id)
            .execute()
        )

        return offer.id
