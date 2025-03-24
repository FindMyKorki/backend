from offers.dataclasses import Offer, CreateOffer, UpdateOffer
from core.db_connection import supabase


class OffersService:
    async def get_offers(self, active_only: bool = False) -> list[Offer]:
        query = supabase.table("offers").select("*")

        if active_only:
            query = query.eq("is_active", True)

        offers = query.execute()
        return offers.data

    async def get_offer(self, offer_id: int) -> Offer:
        offer = (
            supabase.table("offers")
            .select("*")
            .eq("id", offer_id)
            .execute()
        )
        return offer.data[0] if offer.data else None

    async def get_tutor_offers(self, tutor_profile_id: int, active_only: bool = False) -> list[Offer]:
        query = (
            supabase.table("offers")
            .select("*, description:hidden")  # Select all columns except description
            .eq("tutor_profile_id", tutor_profile_id)
        )

        if active_only:
            query = query.eq("is_active", True)

        offers = query.execute()
        return offers.data

    async def create_offer(self, create_offer_data: CreateOffer) -> str:
        new_offer = (
            supabase.table("offers")
            .insert(create_offer_data.model_dump())
            .execute()
        )

        offer_id = new_offer.data[0].get("id")

        return f"Created new offer with id {offer_id}"

    async def update_offer(self, offer_id: int, update_data: UpdateOffer) -> str:
        # Filter out None values
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

        if not update_dict:
            return "No fields to update"

        updated_offer = (
            supabase.table("offers")
            .update(update_dict)
            .eq("id", offer_id)
            .execute()
        )

        return f"Updated offer with id {offer_id}"

    async def delete_offer(self, offer_id: int) -> str:
        deleted_offer = (
            supabase.table("offers")
            .delete()
            .eq("id", offer_id)
            .execute()
        )

        return f"Deleted offer with id {offer_id}"