from datetime import datetime, timedelta, timezone, time
from typing import List, Tuple
from fastapi import HTTPException

from core.db_connection import supabase, get_tutor_unavailabilities, get_tutor_bookings
from .dataclasses import AvailableTimeBlock, TutorAvailabilityResponse
from .utils import subtract_time_blocks, standardize_datetime, parse_recurrence_rule


def merge_overlapping_blocks(blocks: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:
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
    if isinstance(dt, str):
        return datetime.fromisoformat(dt.replace('Z', '+00:00'))
    return standardize_datetime(dt)


class TutorsAvailabilityService:
    MIN_BLOCK_DURATION_MINUTES = 45

    async def get_tutor_available_hours(self, tutor_id: str, start_date: datetime, end_date: datetime) -> TutorAvailabilityResponse:
        try:
            availabilities = await self._get_tutor_availabilities(tutor_id)
            unavailabilities = await self._get_tutor_unavailabilities(tutor_id, start_date, end_date)
            bookings = await self._get_tutor_confirmed_bookings(tutor_id, start_date, end_date)

            availability_blocks = await self._generate_availability_blocks(availabilities, start_date, end_date)

            # Parsowanie unavailabilities na datetime
            unavailability_blocks = []
            for u in unavailabilities:
                start = parse_datetime(u["start_time"])
                end = parse_datetime(u["end_time"])
                unavailability_blocks.append((start, end))

            # Parsowanie bookings na datetime (już zrobione w _get_tutor_confirmed_bookings, ale upewniamy się)
            booking_blocks = []
            for b in bookings:
                start = parse_datetime(b["start_time"]) if isinstance(b["start_time"], str) else b["start_time"]
                end = parse_datetime(b["end_time"]) if isinstance(b["end_time"], str) else b["end_time"]
                booking_blocks.append((start, end))

            available_blocks = subtract_time_blocks(availability_blocks, unavailability_blocks)
            final_blocks = subtract_time_blocks(available_blocks, booking_blocks)
            merged_blocks = merge_overlapping_blocks(final_blocks)

            deduplicated_blocks = []
            seen = set()
            for start, end in merged_blocks:
                key = (start.date().isoformat(), start.time().isoformat(), end.time().isoformat())
                if key not in seen:
                    seen.add(key)
                    deduplicated_blocks.append(AvailableTimeBlock(start_date=start, end_date=end))

            return TutorAvailabilityResponse(available_blocks=deduplicated_blocks)
        except Exception:
            return TutorAvailabilityResponse(available_blocks=[])

    async def _get_tutor_availabilities(self, tutor_id: str):
        try:
            recurring = supabase.table("availabilities").select("*").eq("tutor_id", tutor_id).not_.is_("recurrence_rule", "null").not_.eq("recurrence_rule", "").execute()
            current_time = datetime.now(timezone.utc).isoformat()
            nonrecurring = supabase.table("availabilities").select("*").eq("tutor_id", tutor_id).or_(f"recurrence_rule.is.null,recurrence_rule.eq.").gte("end_time", current_time).execute()
            return recurring.data + nonrecurring.data
        except Exception:
            return []

    async def _get_tutor_unavailabilities(self, tutor_id: str, start_date: datetime, end_date: datetime):
        try:
            return await get_tutor_unavailabilities(tutor_id, start_date, end_date)
        except Exception:
            return []

    async def _get_tutor_confirmed_bookings(self, tutor_id: str, start_date: datetime, end_date: datetime):
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
        except Exception:
            return []

    async def _generate_availability_blocks(self, availabilities, start_date: datetime, end_date: datetime) -> List[Tuple[datetime, datetime]]:
        blocks = []
        for availability in availabilities:
            if "start_time" not in availability or "end_time" not in availability:
                continue
            try:
                avail_start = parse_datetime(availability["start_time"])
                avail_end = parse_datetime(availability["end_time"])
                has_recurrence = "recurrence_rule" in availability and availability["recurrence_rule"]
                avail_day_of_week = avail_start.isoweekday()

                end_date_day = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

                # Dla rekordów z regułą rekurencji sprawdzamy, czy zakres zapytania pokrywa się z okresem rekurencji
                if has_recurrence:
                    # Określamy datę końca rekurencji (UNTIL lub end_date zapytania)
                    rule_dict = parse_recurrence_rule(availability["recurrence_rule"])
                    recurrence_end = end_date_day
                    if "UNTIL" in rule_dict and len(rule_dict["UNTIL"]) >= 8:
                        year, month, day = map(int, [rule_dict["UNTIL"][0:4], rule_dict["UNTIL"][4:6], rule_dict["UNTIL"][6:8]])
                        recurrence_end = min(recurrence_end, datetime(year, month, day, 23, 59, 59, tzinfo=timezone.utc))

                    # Sprawdzamy, czy zakres zapytania pokrywa się z okresem rekurencji
                    if avail_start > end_date_day or recurrence_end < start_date:
                        continue

                    # Punkt startowy iteracji: maksimum z start_date zapytania i start_time dostępności
                    iter_start = max(start_date, avail_start).replace(hour=0, minute=0, second=0, microsecond=0)
                else:
                    # Dla rekordów bez rekurencji iterujemy od start_date zapytania
                    iter_start = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
                    # Jeśli start_time dostępności jest po end_date zapytania, pomijamy
                    if avail_start > end_date_day:
                        continue

                current_date = iter_start
                while current_date <= end_date_day:
                    if (has_recurrence and self._day_matches_recurrence(availability, current_date)) or \
                       (not has_recurrence and current_date.isoweekday() == avail_day_of_week):
                        block_start = datetime.combine(current_date.date(), avail_start.time(), tzinfo=timezone.utc)
                        block_end = datetime.combine(current_date.date(), avail_end.time(), tzinfo=timezone.utc)
                        if block_start <= end_date and block_end >= start_date:
                            blocks.append((max(block_start, start_date), min(block_end, end_date)))
                    current_date += timedelta(days=1)
            except Exception:
                continue
        return merge_overlapping_blocks(blocks)

    def _day_matches_recurrence(self, availability, date):
        if "recurrence_rule" not in availability or not availability["recurrence_rule"]:
            return False
        rule = availability["recurrence_rule"]
        if "BYDAY=" in rule:
            byday = rule.split("BYDAY=")[1].split(";")[0].split(",")
            day_abbrs = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
            return day_abbrs[date.isoweekday() - 1] in byday
        return "FREQ=DAILY" in rule