from core.db_connection import supabase
from crud.crud_provider import CRUDProvider
from enum import Enum
from fastapi import HTTPException
from subjects.service import crud_provider as subject_crud_provider

from .dataclasses import OfferResponse, UpdateOfferRequest, TutorOfferResponse, ActiveOfferResponse, Offer, CreateOffer, \
    UpdateOffer
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
            .execute()
        )

        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Offer not found")

        return flatten_offer_data(response.data[0])

    async def update_offer(self, offer_id: int, request: UpdateOfferRequest, tutor_id: str) -> str:
        await self._check_tutor_exists(tutor_id)
        await self._check_tutor_owns_offer(tutor_id, offer_id)

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

    async def disable_enable_offer(self, offer_id: int, is_active: bool, tutor_id: str) -> str:
        await self._check_tutor_exists(tutor_id)
        await self._check_tutor_owns_offer(tutor_id, offer_id)

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
        await self._check_tutor_exists(tutor_id)

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

    async def get_tutor_offer(self, offer_id: int, tutor_id: str) -> TutorOfferResponse:
        await self._check_tutor_exists(tutor_id)

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

    # CRUD
    async def create_offer(self, tutor_id: str, offer: CreateOffer) -> Offer:
        """
        Create a new offer for a tutor.

        Args:
            tutor_id (str): UUID of the tutor creating the offer.
            offer (CreateOffer): The offer details to be created.

        Returns:
            Offer: The created offer, including any related subjects or entities.
        """
        offer = offer.model_dump()
        offer['tutor_id'] = tutor_id

        new_offer = await offers_crud_provider.create(offer)

        await self.__update_tutor_subjects(new_offer)
        await self.__attach_related_objects(new_offer)

        return Offer.model_validate(new_offer)

    async def get_offer2(self, id: int, tutor_id: str) -> Offer:
        """
        Retrieve a specific offer by ID for a given tutor.

        Args:
            id (int): ID of the offer to retrieve.
            tutor_id (str): UUID of the tutor who owns the offer.

        Returns:
            Offer: The requested offer with related objects attached.
        """
        offer = await offers_crud_provider.get(id, tutor_id)

        await self.__attach_related_objects(offer)

        return Offer.model_validate(offer)

    async def update_offer2(self, tutor_id: str, offer: UpdateOffer) -> Offer:
        """
        Update an existing offer for a tutor.

        Args:
            tutor_id (str): UUID of the tutor updating the offer.
            offer (UpdateOffer): The updated offer data.

        Returns:
            Offer: The updated offer with related subjects and objects attached.
        """
        updated_offer = await offers_crud_provider.update(offer.model_dump(), None, tutor_id)

        await self.__update_tutor_subjects(updated_offer)
        await self.__attach_related_objects(updated_offer)

        return Offer.model_validate(updated_offer)

    async def delete_offer(self, id: int, tutor_id: str) -> Offer:
        """
        Delete a specific offer for a given tutor.

        Args:
            id (int): ID of the offer to delete.
            tutor_id (str): UUID of the tutor who owns the offer.

        Returns:
            Offer: The deleted offer with related objects attached.
        """
        deleted_offer = await offers_crud_provider.delete(id, tutor_id)

        await self.__attach_related_objects(deleted_offer)

        return Offer.model_validate(deleted_offer)

    async def __attach_related_objects(self, offer: dict) -> None:
        if id := offer.get('level_id'):
            level = await levels_crud_provider.get(id)
            offer['level'] = level
        else:
            offer['level'] = None

        if id := offer.get('subject_id'):
            subject = await subject_crud_provider.get(id)
            offer['subject'] = subject
        else:
            offer['subject'] = None

    async def __update_tutor_subjects(self, offer: dict):
        if subject_id := offer.get('subject_id'):
            tutor_id = offer.get('tutor_id')

            try:
                await tutor_subjects_crud_provider.create({
                    'tutor_id': tutor_id,
                    'subject_id': subject_id
                })
            except:
                # Object already exists
                pass

    async def _check_tutor_exists(self, tutor_id: str):
        crud_provider_tutor_profile = CRUDProvider('tutor_profiles', 'tutor_id')
        try:
            await crud_provider_tutor_profile.get(tutor_id)
        except HTTPException as e:
            if e.status_code == 502:
                raise HTTPException(403, f"You are not a tutor!")
            raise

    async def _check_tutor_owns_offer(self, tutor_id: str, offer_id: str):
        crud_offer = CRUDProvider('offers', 'tutor_id')

        try:
            offer = await crud_offer.get(offer_id)
        except HTTPException as e:
            if e.status_code == 404:
                raise HTTPException(404, f"Offer with id {offer_id} not found.")
            elif e.status_code == 502:
                raise HTTPException(502, "No response from query when checking offer.")
            else:
                raise

        if offer.get('tutor_id') != tutor_id:
            raise HTTPException(403, f"This tutor does not own this offer.")
