import logging
from core.db_connection import supabase
from datetime import datetime, timedelta, timezone
from typing import List, Tuple

from .dataclasses import AvailableTimeBlock, TutorAvailabilityResponse
from .utils import subtract_time_blocks, standardize_datetime, generate_occurrences, merge_overlapping_blocks, \
    parse_datetime, generate_availability_blocks

logger = logging.getLogger(__name__)


class TutorsAvailabilityService:
    MIN_BLOCK_DURATION_MINUTES = 45

    async def get_tutor_available_hours(self, tutor_id: str, start_date: datetime,
                                        end_date: datetime) -> TutorAvailabilityResponse:
        try:
            if start_date > end_date:
                raise ValueError("start_date must be before end_date")

            tutor_exists = supabase.table("tutor_profiles").select("id").eq("id", tutor_id).execute()
            if not tutor_exists.data:
                raise ValueError(f"Tutor with id {tutor_id} does not exist")

            start_date = standardize_datetime(start_date)
            end_date = standardize_datetime(end_date)

            availabilities = await self._get_tutor_availabilities(tutor_id)
            unavailabilities = await self._get_tutor_unavailabilities(tutor_id, start_date, end_date)
            bookings = await self._get_tutor_confirmed_bookings(tutor_id, start_date, end_date)

            availability_blocks = await generate_availability_blocks(availabilities, start_date, end_date)

            unavailability_blocks = []
            for u in unavailabilities:
                start = parse_datetime(u["start_time"])
                end = parse_datetime(u["end_time"])
                unavailability_blocks.append((start, end))

            booking_blocks = [(b["start_date"], b["end_date"]) for b in bookings]

            available_blocks = subtract_time_blocks(availability_blocks, unavailability_blocks)
            final_blocks = subtract_time_blocks(available_blocks, booking_blocks)
            merged_blocks = merge_overlapping_blocks(final_blocks)

            min_duration = timedelta(minutes=self.MIN_BLOCK_DURATION_MINUTES)
            filtered_blocks = [
                (start, end) for start, end in merged_blocks
                if (end - start) >= min_duration
            ]

            deduplicated_blocks = []
            seen = set()
            for start, end in filtered_blocks:
                key = (start.date(), start.time(), end.time())
                if key not in seen:
                    seen.add(key)
                    deduplicated_blocks.append(AvailableTimeBlock(start_date=start, end_date=end))

            deduplicated_blocks.sort(key=lambda x: x.start_date)

            return TutorAvailabilityResponse(available_blocks=deduplicated_blocks)
        except ValueError as e:
            logger.error(f"Invalid date range for tutor {tutor_id}: {str(e)}")
            return TutorAvailabilityResponse(available_blocks=[], message=str(e))
        except Exception as e:
            logger.error(f"Unexpected error while fetching available hours for tutor {tutor_id}: {str(e)}")
            return TutorAvailabilityResponse(available_blocks=[])

    async def _get_tutor_availabilities(self, tutor_id: str):
        try:
            recurring = supabase.table("availabilities").select("*").eq("tutor_id", tutor_id).not_.is_(
                "recurrence_rule", "null").not_.eq("recurrence_rule", "").execute()
            current_time = datetime.now(timezone.utc).isoformat()
            nonrecurring = supabase.table("availabilities").select("*").eq("tutor_id", tutor_id).or_(
                f"recurrence_rule.is.null,recurrence_rule.eq.").gte("end_time", current_time).execute()
            availabilities = recurring.data + nonrecurring.data
            return [
                a for a in availabilities
                if a.get("start_time") and a.get("end_time")
            ]
        except Exception as e:
            logger.error(f"Failed to fetch availabilities for tutor {tutor_id}: {str(e)}")
            return []

    async def _get_tutor_unavailabilities(self, tutor_id: str, start_date: datetime, end_date: datetime):
        try:
            unavailabilities = supabase.table("unavailabilities").select("*").eq("tutor_id", tutor_id).gte("start_time",
                                                                                                           start_date.isoformat()).lte(
                "end_time", end_date.isoformat()).execute()
            return [
                u for u in unavailabilities.data
                if u.get("start_time") and u.get("end_time")
            ]
        except Exception as e:
            logger.error(f"Failed to fetch unavailabilities for tutor {tutor_id}: {str(e)}")
            return []

    async def _get_tutor_confirmed_bookings(self, tutor_id: str, start_date: datetime, end_date: datetime):
        try:
            bookings = supabase.table("bookings").select("*, offers!inner(tutor_id)").eq("status", "accepted").eq(
                "offers.tutor_id", tutor_id).gte("start_date", start_date.isoformat()).lte("end_date",
                                                                                           end_date.isoformat()).execute()
            filtered_bookings = []
            for booking in bookings.data:
                if not (booking.get("start_date") and booking.get("end_date")):
                    continue
                start = parse_datetime(booking.get("start_date"))
                end = parse_datetime(booking.get("end_date"))
                filtered_bookings.append({
                    "id": booking.get("id"),
                    "start_date": start,
                    "end_date": end,
                    "offer_id": booking.get("offer_id"),
                    "status": booking.get("status")
                })
            return filtered_bookings
        except Exception as e:
            logger.error(f"Failed to fetch bookings for tutor {tutor_id}: {str(e)}")
            return []
