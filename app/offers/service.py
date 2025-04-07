from .dataclasses import Offer, CreateOffer, UpdateOffer
from crud.crud_provider import CRUDProvider
from subjects.service import crud_provider as subject_crud_provider


offers_crud_provider = CRUDProvider('offers', 'tutor_id')
levels_crud_provider = CRUDProvider('levels')
tutor_subjects_crud_provider = CRUDProvider('tutors_subjects')


class OffersService:
    async def create_offer(self, tutor_id: str, offer: CreateOffer) -> Offer:
        offer = offer.model_dump()
        offer['tutor_id'] = tutor_id

        new_offer = await offers_crud_provider.create(offer)

        await self.__update_tutor_subjects(new_offer)
        await self.__attach_related_objects(new_offer)

        return Offer.model_validate(new_offer)

    async def get_offer(self, id: int, tutor_id: str) -> Offer:
        offer: dict = await offers_crud_provider.get(id, tutor_id)

        await self.__attach_related_objects(offer)

        return Offer.model_validate(offer)

    async def update_offer(self, tutor_id, offer: UpdateOffer) -> Offer:
        updated_offer = await offers_crud_provider.update(offer.model_dump(), None, tutor_id)

        await self.__update_tutor_subjects(updated_offer)
        await self.__attach_related_objects(updated_offer)

        return Offer.model_validate(updated_offer)

    async def delete_offer(self, id: int, tutor_id: str) -> Offer:
        deleted_offer = await offers_crud_provider.delete(id, tutor_id)

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