from datetime import datetime, timezone
from typing import List, Tuple, Dict, Any

from app.tutors_availability.utils import subtract_time_blocks, standardize_datetime


async def subtract_time_blocks_test(
        availability_blocks: List[Tuple[datetime, datetime]],
        unavailabilities: List[Dict[str, Any]]
) -> List[Tuple[datetime, datetime]]:
    parsed_unavailabilities = []
    for unavail in unavailabilities:
        start = unavail.get("start_time")
        end = unavail.get("end_time")
        if start and end:
            start = standardize_datetime(
                datetime.fromisoformat(start.replace('Z', '+00:00')) if isinstance(start, str) else start)
            end = standardize_datetime(
                datetime.fromisoformat(end.replace('Z', '+00:00')) if isinstance(end, str) else end)
            parsed_unavailabilities.append((start, end))
    return subtract_time_blocks(
        [(standardize_datetime(start), standardize_datetime(end)) for start, end in availability_blocks],
        parsed_unavailabilities
    )
