from core.db_connection import supabase
from crud.crud_provider import CRUDProvider
from fastapi import HTTPException

from .dataclasses import AvailabilityHours, UnavailabilityHours

crud_provider = CRUDProvider('availabilities', 'tutor_id')


class AvailabilityService:
    async def get_tutor_availabilities(self, tutor_id: str) -> list[AvailabilityHours]:
        response = (
            supabase
            .table("availabilities")
            .select("start_time, end_time, recurrence_rule")
            .eq("tutor_id", tutor_id)
            .execute()
        )

        if response.data is None or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Offer not found")

        return response.data

    async def create_tutor_availability(self, tutor_id: str, request: AvailabilityHours) -> AvailabilityHours:
        await self._check_tutor_exists(tutor_id)

        data = request.model_dump(mode="json")
        data["tutor_id"] = tutor_id

        created_record = await crud_provider.create(data)
        return created_record

    async def create_tutor_unavailability(self, tutor_id: str, request: UnavailabilityHours) -> UnavailabilityHours:
        await self._check_tutor_exists(tutor_id)

        data = request.model_dump(mode="json")
        data["tutor_id"] = tutor_id

        created_record = supabase.table("unavailabilities").insert(data).execute()
        return created_record.data[0]

    # CRUD
    async def create_availability(self, user_id: str, availability: AvailabilityHours) -> AvailabilityHours:
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

        return AvailabilityHours.model_validate(new_availability)

    async def get_availability(self, id: int, user_id: str) -> AvailabilityHours:
        """
        Retrieve a specific availability slot by ID for a given user.

        Args:
            id (int): The ID of the availability to retrieve.
            user_id (str): The UUID of the user who owns the availability.

        Returns:
            Availability: The requested availability record.
        """
        availability = await crud_provider.get(id, user_id)

        return AvailabilityHours.model_validate(availability)

    async def get_all_availabilitise(self, user_id: str) -> list[AvailabilityHours]:
        """
        Retrieve all availability slots for a given user.

        Args:
            user_id (str): The UUID of the user whose availabilities are to be retrieved.

        Returns:
            list[Availability]: A list of the user's availability records.
        """
        availabilities = await crud_provider.get_all(user_id)

        return [AvailabilityHours.model_validate(a) for a in availabilities]

    async def update_availability(self, user_id, availability: AvailabilityHours) -> AvailabilityHours:
        """
        Update an existing availability slot for a user.

        Args:
            user_id (str): The UUID of the user updating the availability.
            availability (Availability): The updated availability data.

        Returns:
            Availability: The updated availability record.
        """
        updated_availability = await crud_provider.update(availability.model_dump(mode='json'), None, user_id)

        return AvailabilityHours.model_validate(updated_availability)

    async def delete_availability(self, id: int, user_id: str) -> AvailabilityHours:
        """
        Delete a specific availability slot for a given user.

        Args:
            id (int): The ID of the availability to delete.
            user_id (str): The UUID of the user who owns the availability.

        Returns:
            Availability: The deleted availability record.
        """
        deleted_availability = await crud_provider.delete(id, user_id)

        return AvailabilityHours.model_validate(deleted_availability)

    async def _check_tutor_exists(self, tutor_id: str):
        crud_provider_tutor_profile = CRUDProvider('tutor_profiles', 'tutor_id')
        try:
            await crud_provider_tutor_profile.get(tutor_id)
        except HTTPException as e:
            if e.status_code == 502:
                raise HTTPException(403, f"You are not a tutor!")
            raise
