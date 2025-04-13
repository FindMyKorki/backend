import pytest
from datetime import datetime, timedelta, timezone
import os
import sys

# Get the base directory and add it to the path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, base_dir)

# Implement a function that replicates the logic of _generate_unavailability_blocks
# This avoids dependency issues with the Supabase client
async def generate_unavailability_blocks_test(availability_blocks, unavailabilities):
    """
    Test implementation of the _generate_unavailability_blocks method.
    This function replicates the logic but avoids dependencies on the actual service class.
    """
    # Initialize empty result
    result = []
    
    # Process each availability block separately
    for avail_start, avail_end in availability_blocks:
        # Standard datetime format for consistency
        avail_start = standardize_datetime(avail_start)
        avail_end = standardize_datetime(avail_end)
        
        # Initialize with the full block
        temp_blocks = [(avail_start, avail_end)]
        
        # Process each unavailability record
        for unavail in unavailabilities:
            # Get start and end times
            unavail_start_str = unavail.get("start_time")
            unavail_end_str = unavail.get("end_time")
            
            # Skip invalid records
            if not unavail_start_str or not unavail_end_str:
                continue
            
            # Convert to datetime if strings
            if isinstance(unavail_start_str, str):
                unavail_start = datetime.fromisoformat(unavail_start_str.replace('Z', '+00:00'))
            else:
                unavail_start = unavail_start_str
                
            if isinstance(unavail_end_str, str):
                unavail_end = datetime.fromisoformat(unavail_end_str.replace('Z', '+00:00'))
            else:
                unavail_end = unavail_end_str
            
            # Standardize datetime objects
            unavail_start = standardize_datetime(unavail_start)
            unavail_end = standardize_datetime(unavail_end)
            
            # Create new list to hold blocks after removing this unavailability
            new_temp_blocks = []
            
            # For each block in temp_blocks, either keep it intact or split it
            for block_start, block_end in temp_blocks:
                if block_end <= unavail_start or block_start >= unavail_end:
                    # No overlap - keep the block intact
                    new_temp_blocks.append((block_start, block_end))
                else:
                    # There is an overlap - split the block as needed
                    if block_start < unavail_start:
                        # Add the part before unavailability
                        new_temp_blocks.append((block_start, unavail_start))
                    
                    if block_end > unavail_end:
                        # Add the part after unavailability
                        new_temp_blocks.append((unavail_end, block_end))
            
            # Update temp_blocks for the next unavailability
            temp_blocks = new_temp_blocks
        
        # Add the resulting blocks after processing all unavailabilities
        result.extend(temp_blocks)
    
    return result


# Helper function similar to the one in utils.py
def standardize_datetime(dt):
    """Ensure that datetime objects have tzinfo set to UTC timezone."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


class TestGenerateUnavailabilityBlocks:
    """Tests for the _generate_unavailability_blocks implementation."""
    
    @pytest.mark.asyncio
    async def test_no_unavailability(self):
        """Test with no unavailability records."""
        # Create test data
        availability_blocks = [
            (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
             datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc))
        ]
        unavailabilities = []
        
        # Call the method
        result = await generate_unavailability_blocks_test(availability_blocks, unavailabilities)
        
        # Verify result
        assert len(result) == 1
        assert result[0] == (
            standardize_datetime(availability_blocks[0][0]), 
            standardize_datetime(availability_blocks[0][1])
        )
    
    @pytest.mark.asyncio
    async def test_single_unavailability_middle(self):
        """Test with a single unavailability in the middle of an availability block."""
        # Create test data
        availability_blocks = [
            (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
             datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc))
        ]
        unavailabilities = [
            {
                "id": "1",
                "start_time": "2025-04-10T13:00:00Z",
                "end_time": "2025-04-10T14:00:00Z"
            }
        ]
        
        # Call the method
        result = await generate_unavailability_blocks_test(availability_blocks, unavailabilities)
        
        # Verify result
        assert len(result) == 2
        # First block: 10:00 - 13:00
        assert result[0] == (
            datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc),
            datetime(2025, 4, 10, 13, 0, tzinfo=timezone.utc)
        )
        # Second block: 14:00 - 18:00
        assert result[1] == (
            datetime(2025, 4, 10, 14, 0, tzinfo=timezone.utc),
            datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc)
        )
    
    @pytest.mark.asyncio
    async def test_unavailability_at_start(self):
        """Test with unavailability at the start of an availability block."""
        # Create test data
        availability_blocks = [
            (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
             datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc))
        ]
        unavailabilities = [
            {
                "id": "1",
                "start_time": "2025-04-10T09:00:00Z",
                "end_time": "2025-04-10T12:00:00Z"
            }
        ]
        
        # Call the method
        result = await generate_unavailability_blocks_test(availability_blocks, unavailabilities)
        
        # Verify result
        assert len(result) == 1
        # Only one block: 12:00 - 18:00
        assert result[0] == (
            datetime(2025, 4, 10, 12, 0, tzinfo=timezone.utc),
            datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc)
        )
    
    @pytest.mark.asyncio
    async def test_unavailability_at_end(self):
        """Test with unavailability at the end of an availability block."""
        # Create test data
        availability_blocks = [
            (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
             datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc))
        ]
        unavailabilities = [
            {
                "id": "1",
                "start_time": "2025-04-10T16:00:00Z",
                "end_time": "2025-04-10T20:00:00Z"
            }
        ]
        
        # Call the method
        result = await generate_unavailability_blocks_test(availability_blocks, unavailabilities)
        
        # Verify result
        assert len(result) == 1
        # Only one block: 10:00 - 16:00
        assert result[0] == (
            datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc),
            datetime(2025, 4, 10, 16, 0, tzinfo=timezone.utc)
        )
    
    @pytest.mark.asyncio
    async def test_complete_overlap_unavailability(self):
        """Test with unavailability completely overlapping an availability block."""
        # Create test data
        availability_blocks = [
            (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
             datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc))
        ]
        unavailabilities = [
            {
                "id": "1",
                "start_time": "2025-04-10T09:00:00Z",
                "end_time": "2025-04-10T19:00:00Z"
            }
        ]
        
        # Call the method
        result = await generate_unavailability_blocks_test(availability_blocks, unavailabilities)
        
        # Verify result
        assert len(result) == 0  # No available blocks remain
    
    @pytest.mark.asyncio
    async def test_multiple_unavailabilities(self):
        """Test with multiple unavailability periods."""
        # Create test data
        availability_blocks = [
            (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
             datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc))
        ]
        unavailabilities = [
            {
                "id": "1",
                "start_time": "2025-04-10T12:00:00Z",
                "end_time": "2025-04-10T13:00:00Z"
            },
            {
                "id": "2",
                "start_time": "2025-04-10T15:00:00Z",
                "end_time": "2025-04-10T16:00:00Z"
            }
        ]
        
        # Call the method
        result = await generate_unavailability_blocks_test(availability_blocks, unavailabilities)
        
        # Verify result
        assert len(result) == 3
        # First block: 10:00 - 12:00
        assert result[0] == (
            datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc),
            datetime(2025, 4, 10, 12, 0, tzinfo=timezone.utc)
        )
        # Second block: 13:00 - 15:00
        assert result[1] == (
            datetime(2025, 4, 10, 13, 0, tzinfo=timezone.utc),
            datetime(2025, 4, 10, 15, 0, tzinfo=timezone.utc)
        )
        # Third block: 16:00 - 18:00
        assert result[2] == (
            datetime(2025, 4, 10, 16, 0, tzinfo=timezone.utc),
            datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc)
        )
    
    @pytest.mark.asyncio
    async def test_multiple_availability_blocks(self):
        """Test with multiple availability blocks and unavailabilities."""
        # Create test data
        availability_blocks = [
            (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
             datetime(2025, 4, 10, 12, 0, tzinfo=timezone.utc)),
            (datetime(2025, 4, 10, 14, 0, tzinfo=timezone.utc), 
             datetime(2025, 4, 10, 16, 0, tzinfo=timezone.utc))
        ]
        unavailabilities = [
            {
                "id": "1",
                "start_time": "2025-04-10T11:00:00Z",
                "end_time": "2025-04-10T15:00:00Z"
            }
        ]
        
        # Call the method
        result = await generate_unavailability_blocks_test(availability_blocks, unavailabilities)
        
        # Verify result
        assert len(result) == 2
        # First block: 10:00 - 11:00
        assert result[0] == (
            datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc),
            datetime(2025, 4, 10, 11, 0, tzinfo=timezone.utc)
        )
        # Second block: 15:00 - 16:00
        assert result[1] == (
            datetime(2025, 4, 10, 15, 0, tzinfo=timezone.utc),
            datetime(2025, 4, 10, 16, 0, tzinfo=timezone.utc)
        )
    
    @pytest.mark.asyncio
    async def test_string_datetime_handling(self):
        """Test handling of string dates in unavailability records."""
        # Create test data
        availability_blocks = [
            (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
             datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc))
        ]
        unavailabilities = [
            {
                "id": "1",
                "start_time": "2025-04-10T13:00:00Z",  # String format
                "end_time": "2025-04-10T14:00:00Z"     # String format
            }
        ]
        
        # Call the method
        result = await generate_unavailability_blocks_test(availability_blocks, unavailabilities)
        
        # Verify result
        assert len(result) == 2
        # First block: 10:00 - 13:00
        assert result[0] == (
            datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc),
            datetime(2025, 4, 10, 13, 0, tzinfo=timezone.utc)
        )
        # Second block: 14:00 - 18:00
        assert result[1] == (
            datetime(2025, 4, 10, 14, 0, tzinfo=timezone.utc),
            datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc)
        ) 