from .dataclasses import Availability, BaseAvailability
from crud.crud_provider import CRUDProvider


crud_provider = CRUDProvider('availabilities', 'tutor_id')


class AvailabilitiesService:
    async def create_availability(self, user_id: str, availability: BaseAvailability) -> Availability:
        """
        Create a new availability slot for a user.

        Args:
            user_id (str): The UUID of the user (tutor) creating the availability.
            availability (BaseAvailability): The availability details to create.

        Returns:
            Availability: The created availability record.
        """
        availability = availability.model_dump(mode='json')
        availability['tutor_id'] = user_id

        new_availability = await crud_provider.create(availability)

        return Availability.model_validate(new_availability)

    async def get_availability(self, id: int, user_id: str) -> Availability:
        """
        Retrieve a specific availability slot by ID for a given user.

        Args:
            id (int): The ID of the availability to retrieve.
            user_id (str): The UUID of the user who owns the availability.

        Returns:
            Availability: The requested availability record.
        """
        availability = await crud_provider.get(id, user_id)

        return Availability.model_validate(availability)
    
    async def get_all_availabilitise(self, user_id: str) -> list[Availability]:
        """
        Retrieve all availability slots for a given user.

        Args:
            user_id (str): The UUID of the user whose availabilities are to be retrieved.

        Returns:
            list[Availability]: A list of the user's availability records.
        """
        availabilities = await crud_provider.get_all(user_id)

        return [Availability.model_validate(a) for a in availabilities]

    async def update_availability(self, user_id, availability: Availability) -> Availability:
        """
        Update an existing availability slot for a user.

        Args:
            user_id (str): The UUID of the user updating the availability.
            availability (Availability): The updated availability data.

        Returns:
            Availability: The updated availability record.
        """
        updated_availability = await crud_provider.update(availability.model_dump(mode='json'), None, user_id)

        return Availability.model_validate(updated_availability)

    async def delete_availability(self, id: int, user_id: str) -> Availability:
        """
        Delete a specific availability slot for a given user.

        Args:
            id (int): The ID of the availability to delete.
            user_id (str): The UUID of the user who owns the availability.

        Returns:
            Availability: The deleted availability record.
        """
        deleted_availability = await crud_provider.delete(id, user_id)

        return Availability.model_validate(deleted_availability)
