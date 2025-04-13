import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock, Mock
import os

# We need to modify these before importing anything from the app
os.environ['SUPABASE_URL'] = 'https://example.supabase.co'
os.environ['SUPABASE_KEY'] = 'mock_key'

# Mock the imports to avoid the real dependencies
import sys

# Mock psycopg2
sys.modules['psycopg2'] = MagicMock()

# Mock the database connection module
mock_get_tutor_bookings = Mock()
mock_get_tutor_unavailabilities = Mock()
mock_supabase = MagicMock()

sys.modules['app.core.db_connection'] = MagicMock(
    get_tutor_bookings=mock_get_tutor_bookings,
    get_tutor_unavailabilities=mock_get_tutor_unavailabilities,
    supabase=mock_supabase
)

# Now import from app
from app.tutors_availability.service import TutorsAvailabilityService, merge_overlapping_blocks
from app.tutors_availability.dataclasses import AvailableTimeBlock, TutorAvailabilityResponse


@pytest.fixture
def service():
    """Create a TutorsAvailabilityService instance with mocked dependencies."""
    with patch('app.core.db_connection.get_tutor_unavailabilities') as mock_get_unavailabilities, \
         patch('app.core.db_connection.get_tutor_bookings') as mock_get_bookings:
        mock_get_unavailabilities.return_value = []
        mock_get_bookings.return_value = []
        yield TutorsAvailabilityService()


class TestTutorsAvailabilityService:
    
    @pytest.mark.asyncio
    async def test_booking_status_filtering(self, service):
        """Test that confirmed bookings are correctly filtered."""
        # Mock bookings data
        with patch('app.core.db_connection.get_tutor_bookings') as mock_get_bookings:
            mock_bookings = [
                {"booking_id": "1", "status": "CONFIRMED", "start_time": "2023-05-01T10:00:00Z", "end_time": "2023-05-01T11:00:00Z"},
                {"booking_id": "2", "status": "PENDING", "start_time": "2023-05-01T12:00:00Z", "end_time": "2023-05-01T13:00:00Z"},
                {"booking_id": "3", "status": "CANCELLED", "start_time": "2023-05-01T14:00:00Z", "end_time": "2023-05-01T15:00:00Z"},
                {"booking_id": "4", "status": "CONFIRMED", "start_time": "2023-05-01T16:00:00Z", "end_time": "2023-05-01T17:00:00Z"},
            ]
            mock_get_bookings.return_value = mock_bookings
            
            # Get confirmed bookings for a specific date range
            tutor_id = "test_tutor"
            start_date = datetime(2023, 5, 1, tzinfo=timezone.utc)
            end_date = datetime(2023, 5, 2, tzinfo=timezone.utc)
            
            confirmed_bookings = service._get_tutor_confirmed_bookings(tutor_id, start_date, end_date)
            
            # Verify only CONFIRMED bookings are returned
            assert len(confirmed_bookings) == 2
            assert all(booking["status"] == "CONFIRMED" for booking in confirmed_bookings)
            assert any(booking["booking_id"] == "1" for booking in confirmed_bookings)
            assert any(booking["booking_id"] == "4" for booking in confirmed_bookings)
    
    @pytest.mark.asyncio
    async def test_availability_with_bookings_and_unavailability(self, service):
        """Test generating availability blocks with bookings and unavailability."""
        # Mock data
        tutor_id = "test_tutor"
        date = datetime(2023, 5, 1, tzinfo=timezone.utc)
        
        # Mock availability function to return a specific time range
        with patch.object(service, '_get_tutor_availabilities') as mock_get_availabilities, \
             patch('app.core.db_connection.get_tutor_unavailabilities') as mock_get_unavailabilities, \
             patch('app.core.db_connection.get_tutor_bookings') as mock_get_bookings:
            
            # Tutor is available 9 AM - 5 PM
            mock_get_availabilities.return_value = [
                {
                    "day_of_week": date.weekday(),
                    "start_time": "09:00:00",
                    "end_time": "17:00:00",
                    "recurrence_rule": None
                }
            ]
            
            # Tutor has unavailability from 12-1 PM
            mock_get_unavailabilities.return_value = [
                {
                    "id": "1",
                    "start_time": "2023-05-01T12:00:00Z",
                    "end_time": "2023-05-01T13:00:00Z"
                }
            ]
            
            # Tutor has a confirmed booking from 3-4 PM
            mock_get_bookings.return_value = [
                {
                    "booking_id": "1",
                    "status": "CONFIRMED",
                    "start_time": "2023-05-01T15:00:00Z",
                    "end_time": "2023-05-01T16:00:00Z"
                }
            ]
            
            # Get available hours
            start_date = datetime(2023, 5, 1, tzinfo=timezone.utc)
            end_date = datetime(2023, 5, 1, 23, 59, 59, tzinfo=timezone.utc)
            result = service.get_tutor_available_hours(tutor_id, start_date, end_date)
            
            # Verify result structure
            assert isinstance(result, TutorAvailabilityResponse)
            assert len(result.available_time_blocks) == 3
            
            # Expected available blocks after subtracting unavailability and bookings:
            # 9 AM - 12 PM, 1 PM - 3 PM, 4 PM - 5 PM
            blocks = sorted(result.available_time_blocks, key=lambda b: b.start_time)
            
            # First block: 9 AM - 12 PM
            assert blocks[0].start_time.hour == 9
            assert blocks[0].end_time.hour == 12
            
            # Second block: 1 PM - 3 PM
            assert blocks[1].start_time.hour == 13
            assert blocks[1].end_time.hour == 15
            
            # Third block: 4 PM - 5 PM
            assert blocks[2].start_time.hour == 16
            assert blocks[2].end_time.hour == 17


class TestMergeOverlappingBlocks:
    
    def test_merge_overlapping_blocks(self):
        """Test merging overlapping time blocks"""
        
        # Test no blocks
        assert merge_overlapping_blocks([]) == []
        
        # Test single block
        block = (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
                datetime(2025, 4, 10, 12, 0, tzinfo=timezone.utc))
        assert merge_overlapping_blocks([block]) == [block]
        
        # Test non-overlapping blocks
        block1 = (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
                 datetime(2025, 4, 10, 12, 0, tzinfo=timezone.utc))
        block2 = (datetime(2025, 4, 10, 14, 0, tzinfo=timezone.utc), 
                 datetime(2025, 4, 10, 16, 0, tzinfo=timezone.utc))
        assert merge_overlapping_blocks([block1, block2]) == [block1, block2]
        
        # Test overlapping blocks
        block1 = (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
                 datetime(2025, 4, 10, 12, 0, tzinfo=timezone.utc))
        block2 = (datetime(2025, 4, 10, 11, 0, tzinfo=timezone.utc), 
                 datetime(2025, 4, 10, 13, 0, tzinfo=timezone.utc))
        expected = [(datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
                    datetime(2025, 4, 10, 13, 0, tzinfo=timezone.utc))]
        assert merge_overlapping_blocks([block1, block2]) == expected
        
        # Test consecutive blocks
        block1 = (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
                 datetime(2025, 4, 10, 12, 0, tzinfo=timezone.utc))
        block2 = (datetime(2025, 4, 10, 12, 0, tzinfo=timezone.utc), 
                 datetime(2025, 4, 10, 14, 0, tzinfo=timezone.utc))
        expected = [(datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
                    datetime(2025, 4, 10, 14, 0, tzinfo=timezone.utc))]
        assert merge_overlapping_blocks([block1, block2]) == expected 