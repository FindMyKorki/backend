from datetime import datetime, timedelta, timezone
from typing import List, Tuple
import logging

from core.db_connection import supabase, get_tutor_unavailabilities, get_tutor_bookings
from .dataclasses import AvailableTimeBlock, TutorAvailabilityResponse
from .utils import subtract_time_blocks, standardize_datetime, generate_occurrences

logger = logging.getLogger(__name__)

def merge_overlapping_blocks(blocks: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:
    """
    Merge overlapping time blocks into a single block.

    Args:
        blocks (List[Tuple[datetime, datetime]]): List of time blocks to merge.

    Returns:
        List[Tuple[datetime, datetime]]: List of merged time blocks.
    """
    if not blocks:
        return []
    sorted_blocks = sorted(blocks, key=lambda x: x[0])
    result = [sorted_blocks[0]]
    for current_start, current_end in sorted_blocks[1:]:
        prev_start, prev_end = result[-1]
        if current_start <= prev_end:
            result[-1] = (prev_start, max(prev_end, current_end))
        else:
            result.append((current_start, current_end))
    return result


def parse_datetime(dt: str | datetime) -> datetime:
    """
    Parse a datetime string or standardize a datetime object to UTC.

    Args:
        dt (str | datetime): Datetime string or object to parse.

    Returns:
        datetime: Parsed datetime object in UTC.
    """
    if isinstance(dt, str):
        return datetime.fromisoformat(dt.replace('Z', '+00:00'))
    return standardize_datetime(dt)


class TutorsAvailabilityService:
    async def get_tutor_available_hours(self, tutor_id: str, start_date: datetime, end_date: datetime) -> TutorAvailabilityResponse:
        """
        Retrieve available time blocks for a tutor within a specified date range.

        Args:
            tutor_id (str): The ID of the tutor.
            start_date (datetime): The start of the query range (inclusive).
            end_date (datetime): The end of the query range (inclusive).

        Returns:
            TutorAvailabilityResponse: A response containing the list of available time blocks.
        """
        try:
            if start_date > end_date:
                raise ValueError("start_date must be before end_date")

            availabilities = await self._get_tutor_availabilities(tutor_id)
            unavailabilities = await self._get_tutor_unavailabilities(tutor_id, start_date, end_date)
            bookings = await self._get_tutor_confirmed_bookings(tutor_id, start_date, end_date)

            availability_blocks = await self._generate_availability_blocks(availabilities, start_date, end_date)

            unavailability_blocks = []
            for u in unavailabilities:
                start = parse_datetime(u["start_time"])
                end = parse_datetime(u["end_time"])
                unavailability_blocks.append((start, end))

            booking_blocks = [(b["start_time"], b["end_time"]) for b in bookings]

            available_blocks = subtract_time_blocks(availability_blocks, unavailability_blocks)
            final_blocks = subtract_time_blocks(available_blocks, booking_blocks)
            merged_blocks = merge_overlapping_blocks(final_blocks)

            deduplicated_blocks = []
            seen = set()
            for start, end in merged_blocks:
                key = (start, end)
                if key not in seen:
                    seen.add(key)
                    deduplicated_blocks.append(AvailableTimeBlock(start_date=start, end_date=end))

            return TutorAvailabilityResponse(available_blocks=deduplicated_blocks)
        except ValueError as e:
            logger.error(f"Invalid date range for tutor {tutor_id}: {str(e)}")
            return TutorAvailabilityResponse(available_blocks=[], message=str(e))
        except Exception as e:
            logger.error(f"Unexpected error while fetching available hours for tutor {tutor_id}: {str(e)}")
            return TutorAvailabilityResponse(available_blocks=[])

    async def _get_tutor_availabilities(self, tutor_id: str):
        """
        Fetch tutor availabilities from the database.

        Args:
            tutor_id (str): The ID of the tutor.

        Returns:
            List[dict]: List of availability records.
        """
        try:
            recurring = supabase.table("availabilities").select("*").eq("tutor_id", tutor_id).not_.is_("recurrence_rule", "null").not_.eq("recurrence_rule", "").execute()
            current_time = datetime.now(timezone.utc).isoformat()
            nonrecurring = supabase.table("availabilities").select("*").eq("tutor_id", tutor_id).or_(f"recurrence_rule.is.null,recurrence_rule.eq.").gte("end_time", current_time).execute()
            return recurring.data + nonrecurring.data
        except Exception as e:
            logger.error(f"Failed to fetch availabilities for tutor {tutor_id}: {str(e)}")
            return []

    async def _get_tutor_unavailabilities(self, tutor_id: str, start_date: datetime, end_date: datetime):
        """
        Fetch tutor unavailabilities from the database.

        Args:
            tutor_id (str): The ID of the tutor.
            start_date (datetime): Start of the query range.
            end_date (datetime): End of the query range.

        Returns:
            List[dict]: List of unavailability records.
        """
        try:
            return await get_tutor_unavailabilities(tutor_id, start_date, end_date)
        except Exception as e:
            logger.error(f"Failed to fetch unavailabilities for tutor {tutor_id}: {str(e)}")
            return []

    async def _get_tutor_confirmed_bookings(self, tutor_id: str, start_date: datetime, end_date: datetime):
        """
        Fetch confirmed bookings for a tutor within a date range.

        Args:
            tutor_id (str): The ID of the tutor.
            start_date (datetime): Start of the query range.
            end_date (datetime): End of the query range.

        Returns:
            List[dict]: List of confirmed booking records.
        """
        try:
            all_bookings = get_tutor_bookings(tutor_id)
            filtered_bookings = []
            for booking in all_bookings:
                start = parse_datetime(booking.get("start_time"))
                end = parse_datetime(booking.get("end_time"))
                if start and end and (
                    (start >= start_date and start <= end_date) or
                    (end >= start_date and end <= end_date) or
                    (start <= start_date and end >= end_date)
                ):
                    filtered_bookings.append({
                        "id": booking.get("id"),
                        "start_time": start,
                        "end_time": end,
                        "offer_id": booking.get("offer_id"),
                        "status": booking.get("status")
                    })
            return filtered_bookings
        except Exception as e:
            logger.error(f"Failed to fetch bookings for tutor {tutor_id}: {str(e)}")
            return []

    async def _generate_availability_blocks(self, availabilities, start_date: datetime, end_date: datetime) -> List[Tuple[datetime, datetime]]:
        """
        Generate availability blocks based on tutor availabilities and recurrence rules.

        Args:
            availabilities (List[dict]): List of availability records.
            start_date (datetime): Start of the query range.
            end_date (datetime): End of the query range.

        Returns:
            List[Tuple[datetime, datetime]]: List of generated availability blocks.
        """
        blocks = []
        for availability in availabilities:
            if "start_time" not in availability or "end_time" not in availability:
                continue
            try:
                avail_start = parse_datetime(availability["start_time"])
                avail_end = parse_datetime(availability["end_time"])
                recurrence_rule = availability.get("recurrence_rule", "")

                occurrences = generate_occurrences(
                    start_date=avail_start,
                    end_date=avail_end,
                    recurrence_rule=recurrence_rule,
                    query_start=start_date,
                    query_end=end_date
                )

                for block_start, block_end in occurrences:
                    if block_start <= end_date and block_end >= start_date:
                        blocks.append((max(block_start, start_date), min(block_end, end_date)))
            except Exception as e:
                logger.error(f"Failed to generate availability blocks: {str(e)}")
                continue
        return merge_overlapping_blocks(blocks)
