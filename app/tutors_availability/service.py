from datetime import datetime, timedelta
from typing import List, Tuple

from core.db_connection import supabase
from .dataclasses import AvailableTimeBlock, TutorAvailabilityResponse
from .utils import generate_occurrences, subtract_time_blocks, standardize_datetime


class TutorsAvailabilityService:
    MIN_BLOCK_DURATION_MINUTES = 45

    async def get_tutor_available_hours(self, tutor_id: str, start_date: datetime, end_date: datetime) -> TutorAvailabilityResponse:
        """
        Retrieves available time blocks for a tutor within a specified date range
        
        Args:
            tutor_id: Tutor's ID
            start_date: Start date of the range
            end_date: End date of the range
            
        Returns:
            TutorAvailabilityResponse containing a list of available time blocks
        """
        start_date = standardize_datetime(start_date)
        end_date = standardize_datetime(end_date) if end_date else None
        
        availabilities = await self._get_tutor_availabilities(tutor_id)
        unavailabilities = await self._get_tutor_unavailabilities(tutor_id)
        bookings = await self._get_tutor_confirmed_bookings(tutor_id)
        
        availability_blocks = self._generate_availability_blocks(availabilities, start_date, end_date)
        unavailability_blocks = self._generate_unavailability_blocks(unavailabilities, start_date, end_date)
        booking_blocks = self._generate_booking_blocks(bookings, start_date, end_date)
        
        available_blocks = availability_blocks
        if unavailability_blocks:
            available_blocks = subtract_time_blocks(available_blocks, unavailability_blocks)
        
        if booking_blocks:
            available_blocks = subtract_time_blocks(available_blocks, booking_blocks)
        
        min_duration = timedelta(minutes=self.MIN_BLOCK_DURATION_MINUTES)
        filtered_blocks = [
            (start, end) for start, end in available_blocks
            if (end - start) >= min_duration
        ]
        
        result_blocks = [
            AvailableTimeBlock(start_date=start, end_date=end)
            for start, end in filtered_blocks
        ]
        
        return TutorAvailabilityResponse(available_blocks=result_blocks)
    
    async def _get_tutor_availabilities(self, tutor_id: str):
        """Retrieves all availabilities for a tutor from the database"""
        availabilities = (
            supabase.table("availabilities")
            .select("*")
            .eq("tutor_id", tutor_id)
            .execute()
        )
        return availabilities.data
    
    async def _get_tutor_unavailabilities(self, tutor_id: str):
        """Retrieves all unavailabilities for a tutor from the database"""
        try:
            unavailabilities = (
                supabase.table("unavailabilities")
                .select("*")
                .eq("tutor_id", tutor_id)
                .execute()
            )
            return unavailabilities.data
        except Exception:
            return []
    
    async def _get_tutor_confirmed_bookings(self, tutor_id: str):
        """Retrieves all confirmed bookings for a tutor from the database"""
        bookings = (
            supabase.table("bookings")
            .select("*")
            .eq("status", "confirmed")
            .execute()
        )
        
        confirmed_bookings = []
        for booking in bookings.data:
            offer_id = booking.get("offer_id")
            if offer_id:
                offer = (
                    supabase.table("offers")
                    .select("*")
                    .eq("id", offer_id)
                    .eq("tutor_id", tutor_id)
                    .execute()
                )
                if offer.data and len(offer.data) > 0:
                    confirmed_bookings.append(booking)
        
        return confirmed_bookings
    
    def _generate_availability_blocks(self, availabilities, start_date: datetime, end_date: datetime) -> List[Tuple[datetime, datetime]]:
        """Generates all availability blocks for a tutor within the specified date range"""
        result = []
        
        for availability in availabilities:
            avail_start = standardize_datetime(datetime.fromisoformat(availability.get("start_time")))
            avail_end = standardize_datetime(datetime.fromisoformat(availability.get("end_time")))
            recurrence_rule = availability.get("recurrence_rule", "")
            
            occurrences = generate_occurrences(
                avail_start, avail_end, recurrence_rule, start_date, end_date
            )
            
            result.extend(occurrences)
        
        return result
    
    def _generate_unavailability_blocks(self, unavailabilities, start_date: datetime, end_date: datetime) -> List[Tuple[datetime, datetime]]:
        """Generates all unavailability blocks for a tutor within the specified date range"""
        result = []
        
        for unavailability in unavailabilities:
            unavail_start = standardize_datetime(datetime.fromisoformat(unavailability.get("start_time")))
            unavail_end = standardize_datetime(datetime.fromisoformat(unavailability.get("end_time")))
            
            if unavail_end > start_date and unavail_start < end_date:
                adjusted_start = max(unavail_start, start_date)
                adjusted_end = min(unavail_end, end_date)
                result.append((adjusted_start, adjusted_end))
        
        return result
    
    def _generate_booking_blocks(self, bookings, start_date: datetime, end_date: datetime) -> List[Tuple[datetime, datetime]]:
        """Generates all booking blocks for a tutor within the specified date range"""
        result = []
        
        for booking in bookings:
            booking_start = standardize_datetime(datetime.fromisoformat(booking.get("start_date")))
            booking_end = standardize_datetime(datetime.fromisoformat(booking.get("end_date")))
            
            if booking_end > start_date and booking_start < end_date:
                adjusted_start = max(booking_start, start_date)
                adjusted_end = min(booking_end, end_date)
                result.append((adjusted_start, adjusted_end))
        
        return result 