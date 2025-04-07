from .dataclasses import Availability, CreateAvailabilityRequest
from crud.crud_provider import CRUDProvider


crud_provider = CRUDProvider('availabilities', 'tutor_id')


class AvailabilitiesService:
    async def create_availability(self, user_id: str, availability: CreateAvailabilityRequest) -> Availability:
        availability = availability.model_dump(mode='json')
        availability['tutor_id'] = user_id

        new_availability = await crud_provider.create(availability)

        return Availability.model_validate(new_availability)

    async def get_availability(self, id: int, user_id: str) -> Availability:
        availability: dict = await crud_provider.get(id, user_id)

        return Availability.model_validate(availability)
    
    async def get_all_availabilitise(self, user_id: str) -> list[Availability]:
        availabilities = await crud_provider.get_all(user_id)

        return [Availability.model_validate(a) for a in availabilities]

    async def update_availability(self, user_id, availability: Availability) -> Availability:
        updated_availability = await crud_provider.update(availability.model_dump(mode='json'), None, user_id)

        return Availability.model_validate(updated_availability)

    async def delete_availability(self, id: int, user_id: str) -> Availability:
        deleted_availability = await crud_provider.delete(id, user_id)

        return Availability.model_validate(deleted_availability)
