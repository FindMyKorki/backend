from .dataclasses import Unavailability, CreateUnavailabilityRequest
from crud.crud_provider import CRUDProvider


crud_provider = CRUDProvider('unavailabilities', 'tutor_id')


class UnavailabilitiesService:
    async def create_unavailability(self, user_id: str, unavailability: CreateUnavailabilityRequest) -> Unavailability:
        unavailability = unavailability.model_dump(mode='json')
        unavailability['tutor_id'] = user_id

        new_unavailability = await crud_provider.create(unavailability)

        return Unavailability.model_validate(new_unavailability)

    async def get_unavailability(self, id: int, user_id: str) -> Unavailability:
        unavailability: dict = await crud_provider.get(id, user_id)

        return Unavailability.model_validate(unavailability)

    async def get_all_unavailabilities(self, user_id: str) -> list[Unavailability]:
        unavailabilities = await crud_provider.get_all(user_id)

        return [Unavailability.model_validate(u) for u in unavailabilities]

    async def update_unavailability(self, user_id, unavailability: Unavailability) -> Unavailability:
        updated_unavailability = await crud_provider.update(unavailability.model_dump(mode='json'), None, user_id)

        return Unavailability.model_validate(updated_unavailability)

    async def delete_unavailability(self, id: int, user_id: str) -> Unavailability:
        deleted_unavailability = await crud_provider.delete(id, user_id)

        return Unavailability.model_validate(deleted_unavailability)
