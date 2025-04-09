from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import AvailabilityHours, UnavailabilityHours


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

    async def create_tutor_availability(self, tutor_id: str, request: AvailabilityHours) -> str:
        data = request.model_dump(mode="json")
        data["tutor_id"] = tutor_id

        supabase.table("availabilities").insert(data).execute()
        return 'Tutor availability created successfully'

    async def create_tutor_unavailability(self, tutor_id: str, request: UnavailabilityHours) -> str:
        data = request.model_dump(mode="json")
        data["tutor_id"] = tutor_id

        supabase.table("unavailabilities").insert(data).execute()
        return 'Tutor unavailability created successfully'
