from datetime import datetime, timedelta
from typing import Optional

from core.db_connection import supabase
from crud.crud_provider import CRUDProvider
from enum import Enum
from fastapi import HTTPException
from subjects.service import crud_provider as subject_crud_provider

from .dataclasses import OfferResponse, UpdateOfferRequest, TutorOfferResponse, ActiveOfferResponse, Offer, CreateOffer, \
    UpdateOffer
from .utils import flatten_offer_data, flatten_tutor_offers_data, flatten_tutor_offer_data, flatten_active_offers


class Order(str, Enum):
    increasing = "ASC"
    decreasing = "DESC"


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
            .select("id, tutor_id, price, description, subjects(name, icon_url), levels(level), is_active")
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
            .select("id, tutor_id, price, description, subjects(name, icon_url), levels(level), is_active")
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
            .select("id, tutor_id, price, title, description, subjects(name, icon_url), levels(level), is_active")
            .eq("tutor_id", tutor_id)
            .eq("is_active", True)
            .execute()
        )

        if offers.data is None or len(offers.data) == 0:
            raise HTTPException(status_code=404, detail="Offers not found")

        return flatten_tutor_offers_data(offers.data)

    async def get_active_offers(self, level_id: int, subject_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, min_price: Optional[float] = None, max_price: Optional[float] = None, order: Optional[str] = 'ASC', limit: Optional[int] = 5, offset: Optional[int] = 0) -> list[ActiveOfferResponse]:


        filtered_offers = supabase.rpc('filter_offers', {
            'p_level_id': level_id,
            'p_subject_id': subject_id,
            'p_start_date': start_date,
            'p_end_date': end_date,
            'p_min_price': min_price,
            'p_max_price': max_price,
            'p_sort_order': order,
            'p_limit': limit,
            'p_offset': offset
        }).execute()

        return filtered_offers.data

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
