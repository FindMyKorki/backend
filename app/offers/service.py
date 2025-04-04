from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import OfferResponse, UpdateOfferRequest, TutorOfferResponse, ActiveOfferResponse
from .utils import flatten_offer_data, flatten_tutor_offers_data, flatten_tutor_offer_data, flatten_active_offers


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

    async def disable_enable_offer(self, offer_id: int, is_active: bool) -> int:
        service = OffersService()
        offer = await service.get_offer(offer_id)

        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")
        update_offer = (
            supabase
            .table("offers")
            .update({"is_active": is_active})
            .eq("id", offer_id)
            .execute()
        )

        return offer.id

    async def get_tutor_offers(self, tutor_id: str) -> list[TutorOfferResponse]:
        offers = (
            supabase
            .table("offers")
            .select("id, price, subjects(name:subject_name, icon_url), levels(level), is_active")
            .eq("tutor_id", str(tutor_id))
            .execute()
        )

        if offers.data is None or len(offers.data) == 0:
            raise HTTPException(status_code=404, detail="Offers not found")

        return flatten_tutor_offers_data(offers.data)

    async def get_tutor_offer(self, offer_id: int) -> TutorOfferResponse:
        offers = (
            supabase
            .table("offers")
            .select("id, price, subjects(name:subject_name, icon_url), levels(level), is_active")
            .eq("id", offer_id)
            .execute()
        )

        if offers.data is None or len(offers.data) == 0:
            raise HTTPException(status_code=404, detail="Offers not found")

        return flatten_tutor_offer_data(offers.data[0])

    async def get_tutor_active_offer(self, tutor_id: str) -> list[TutorOfferResponse]:
        offers = (
            supabase
            .table("offers")
            .select("id, price, subjects(name:subject_name, icon_url), levels(level), is_active")
            .eq("tutor_id", tutor_id)
            .eq("is_active", True)
            .execute()
        )

        if offers.data is None or len(offers.data) == 0:
            raise HTTPException(status_code=404, detail="Offers not found")

        return flatten_tutor_offers_data(offers.data)

    async def get_active_offers(self, sort_by: str, order: str) -> list[ActiveOfferResponse]:
        offers = (
            supabase
            .table("offers")
            .select(
                "id, price, "
                "tutor_profiles(rating, profiles(full_name, avatar_url)), "
                "subjects(name:subject_name, icon_url), "
                "levels(level)"
            )
            .eq("is_active", True)
            .execute()
        )

        if offers.data is None or len(offers.data) == 0:
            raise HTTPException(status_code=404, detail="Offers not found")

        return flatten_active_offers(offers.data)
