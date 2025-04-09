from core.db_connection import supabase
from enum import Enum
from fastapi import HTTPException

from .dataclasses import OfferResponse, UpdateOfferRequest, TutorOfferResponse, ActiveOfferResponse
from .utils import flatten_offer_data, flatten_tutor_offers_data, flatten_tutor_offer_data, flatten_active_offers


class SortBy(str, Enum):
    rating = "rating"
    price = "price"
    name = "name"


class Order(str, Enum):
    increasing = "increasing"
    decreasing = "decreasing"


class OffersService:
    async def get_offer(self, offer_id: int) -> OfferResponse:
        response = (
            supabase
            .table("offers")
            .select(
                "id, description, price, "
                "tutor_profiles(id, rating, profiles(full_name, avatar_url)), "
                "subjects(name, icon_url), "
                "levels(level)"
            )
            .eq("id", offer_id)
            .single()
            .execute()
        )

        if response.data is None:
            raise HTTPException(status_code=404, detail="Offer not found")

        return flatten_offer_data(response.data)

    async def update_offer(self, offer_id: int, request: UpdateOfferRequest) -> str:
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

        return f"Offer id:{offer.id} updated"

    async def disable_enable_offer(self, offer_id: int, is_active: bool) -> str:
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

        return f"Offer id: {offer.id} {"enabled" if is_active else "disabled"}"

    async def get_tutor_offers(self, tutor_id: str) -> list[TutorOfferResponse]:
        offers = (
            supabase
            .table("offers")
            .select("id, price, subjects(name, icon_url), levels(level), is_active")
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
            .select("id, price, subjects(name, icon_url), levels(level), is_active")
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
            .select("id, price, subjects(name, icon_url), levels(level), is_active")
            .eq("tutor_id", tutor_id)
            .eq("is_active", True)
            .execute()
        )

        if offers.data is None or len(offers.data) == 0:
            raise HTTPException(status_code=404, detail="Offers not found")

        return flatten_tutor_offers_data(offers.data)

    async def get_active_offers(self, sort_by: str, order: str) -> list[ActiveOfferResponse]:
        order_map = {
            SortBy.rating: ("rating", "tutor_profiles"),
            SortBy.price: ("price", None),
            SortBy.name: ("full_name", "tutor_profiles.profiles")
        }

        if sort_by not in order_map:
            raise HTTPException(status_code=400, detail="Invalid sort_by value")

        column, foreign_table = order_map[sort_by]
        sort_desc = order == Order.decreasing

        query = (
            supabase
            .table("offers")
            .select(
                "id, price, "
                "tutor_profiles(rating, profiles(full_name, avatar_url)), "
                "subjects(name, icon_url), "
                "levels(level)"
            )
            .eq("is_active", True)

        )

        if foreign_table:
            query = query.order(column, desc=sort_desc, foreign_table=foreign_table)
        else:
            query = query.order(column, desc=sort_desc)

        offers = query.execute()

        if offers.data is None or len(offers.data) == 0:
            raise HTTPException(status_code=404, detail="Offers not found")

        return flatten_active_offers(offers.data)
