from crud.crud_provider import CRUDProvider

from .dataclasses import Unavailability, BaseUnavailability

crud_provider = CRUDProvider('unavailabilities', 'tutor_id')


class UnavailabilitiesService:
    async def create_unavailability(self, user_id: str, unavailability: BaseUnavailability) -> Unavailability:
        """
        Create a new unavailability slot for a tutor.

        Args:
            user_id (str): UUID of the tutor marking themselves unavailable.
            unavailability (BaseUnavailability): The unavailability details to be created.

        Returns:
            Unavailability: The created unavailability record.
        """
        unavailability = unavailability.model_dump(mode='json')
        unavailability['tutor_id'] = user_id

        new_unavailability = await crud_provider.create(unavailability)

        return Unavailability.model_validate(new_unavailability)

    async def get_unavailability(self, id: int, user_id: str) -> Unavailability:
        """
        Retrieve a specific unavailability slot by ID for a given tutor.

        Args:
            id (int): ID of the unavailability record to retrieve.
            user_id (str): UUID of the tutor who owns the record.

        Returns:
            Unavailability: The requested unavailability record.
        """
        unavailability = await crud_provider.get(id, user_id)

        return Unavailability.model_validate(unavailability)

    async def get_all_unavailabilities(self, user_id: str) -> list[Unavailability]:
        """
        Retrieve all unavailability slots for a specific tutor.

        Args:
            user_id (str): UUID of the tutor whose unavailabilities are being fetched.

        Returns:
            list[Unavailability]: A list of all unavailability records for the tutor.
        """
        unavailabilities = await crud_provider.get_all(user_id)

        return [Unavailability.model_validate(u) for u in unavailabilities]

    async def update_unavailability(self, user_id: str, unavailability: Unavailability) -> Unavailability:
        """
        Update an existing unavailability slot for a tutor.

        Args:
            user_id (str): UUID of the tutor updating the record.
            unavailability (Unavailability): The updated unavailability data.

        Returns:
            Unavailability: The updated unavailability record.
        """
        updated_unavailability = await crud_provider.update(
            unavailability.model_dump(mode='json'), None, user_id
        )

        return Unavailability.model_validate(updated_unavailability)

    async def delete_unavailability(self, id: int, user_id: str) -> Unavailability:
        """
        Delete a specific unavailability slot for a tutor.

        Args:
            id (int): ID of the unavailability record to delete.
            user_id (str): UUID of the tutor who owns the record.

        Returns:
            Unavailability: The deleted unavailability record.
        """
        deleted_unavailability = await crud_provider.delete(id, user_id)

        return Unavailability.model_validate(deleted_unavailability)
