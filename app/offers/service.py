from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import OfferResponse
from .utils import flatten_offer_data


class OffersService:
    async def get_offers(self, offer_id: int) -> OfferResponse:
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
