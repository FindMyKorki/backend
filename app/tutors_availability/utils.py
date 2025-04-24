import calendar
from datetime import datetime, timedelta, timezone, date
from typing import List, Tuple


def standardize_datetime(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(
        timezone.utc) if dt.tzinfo != timezone.utc else dt


def parse_recurrence_rule(rule: str) -> dict:
    if not rule:
        return {}
    result = {}
    for part in rule.split(';'):
        if '=' in part:
            key, value = part.split('=')
            if key in ['FREQ', 'UNTIL', 'COUNT']:
                result[key] = value
            elif key == 'INTERVAL':
                result[key] = int(value)
            elif key in ['BYDAY', 'BYMONTHDAY', 'BYMONTH']:
                result[key] = value.split(',')
    return result


def get_weekday_num(day_code: str) -> int:
    days = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}
    return days.get(day_code, 0)


def generate_occurrences(start_date: datetime, end_date: datetime, recurrence_rule: str, query_start: datetime,
                         query_end: datetime) -> List[Tuple[datetime, datetime]]:
    start_date = standardize_datetime(start_date)
    end_date = standardize_datetime(end_date)
    query_start = standardize_datetime(query_start)
    query_end = standardize_datetime(query_end)
    result = []

    if not recurrence_rule:
        if start_date <= query_end and end_date >= query_start:
            result.append((start_date, end_date))
        return result

    rule_dict = parse_recurrence_rule(recurrence_rule)
    freq = rule_dict.get('FREQ')
    interval = rule_dict.get('INTERVAL', 1)
    until_date = query_end

    if 'UNTIL' in rule_dict and len(rule_dict['UNTIL']) >= 8:
        year, month, day = map(int, [rule_dict['UNTIL'][0:4], rule_dict['UNTIL'][4:6], rule_dict['UNTIL'][6:8]])
        until_date = min(until_date, datetime(year, month, day, 23, 59, 59, tzinfo=timezone.utc))

    duration = end_date - start_date

    if freq == 'DAILY':
        current_date = start_date
        if current_date < query_start:
            days_to_add = ((query_start - current_date).days // interval) * interval
            current_date += timedelta(days=days_to_add)
        while current_date <= until_date:
            event_end = current_date + duration
            if event_end >= query_start:
                result.append((current_date, event_end))
            current_date += timedelta(days=interval)

    elif freq == 'WEEKLY':
        weekdays = [get_weekday_num(day) for day in rule_dict.get('BYDAY', [])] or [start_date.weekday()]
        base_date = start_date
        if base_date < query_start:
            weeks_to_add = (((query_start - base_date).days // 7) // interval) * interval
            base_date += timedelta(days=weeks_to_add * 7)
        current_week_start = base_date - timedelta(days=base_date.weekday())
        while current_week_start <= until_date:
            for weekday in weekdays:
                current_date = current_week_start + timedelta(days=weekday)
                current_date = current_date.replace(hour=base_date.hour, minute=base_date.minute,
                                                    second=base_date.second, microsecond=base_date.microsecond)
                event_end = current_date + duration
                if event_end >= query_start:
                    result.append((current_date, event_end))
            current_week_start += timedelta(days=7 * interval)

    elif freq == 'MONTHLY':
        current_date = start_date
        if current_date < query_start:
            months_diff = (query_start.year - current_date.year) * 12 + query_start.month - current_date.month
            months_to_add = (months_diff // interval) * interval
            if months_to_add:
                new_month = ((current_date.month - 1 + months_to_add) % 12) + 1
                new_year = current_date.year + (current_date.month - 1 + months_to_add) // 12
                max_day = 30 if new_month in [4, 6, 9, 11] else 29 if new_month == 2 and (new_year % 4 == 0 and (
                            new_year % 100 != 0 or new_year % 400 == 0)) else 28 if new_month == 2 else 31
                current_date = current_date.replace(year=new_year, month=new_month, day=min(current_date.day, max_day))
        while current_date <= until_date:
            if (not rule_dict.get('BYMONTHDAY') or str(current_date.day) in rule_dict['BYMONTHDAY']) and (
                    not rule_dict.get('BYMONTH') or str(current_date.month) in rule_dict['BYMONTH']):
                event_end = current_date + duration
                if event_end >= query_start:
                    result.append((current_date, event_end))
            month = current_date.month - 1 + interval
            year = current_date.year + month // 12
            month = month % 12 + 1
            max_day = 30 if month in [4, 6, 9, 11] else 29 if month == 2 and (
                        year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28 if month == 2 else 31
            day = min(current_date.day, max_day)
            try:
                current_date = current_date.replace(year=year, month=month, day=day)
            except ValueError:
                current_date = current_date.replace(year=year, month=month, day=max_day)

    return result


def subtract_time_blocks(base_blocks: List[Tuple[datetime, datetime]],
                         subtract_blocks: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:
    result = []
    for base_start, base_end in base_blocks:
        current_blocks = [(base_start, base_end)]
        for sub_start, sub_end in subtract_blocks:
            new_blocks = []
            for block_start, block_end in current_blocks:
                if sub_end <= block_start or sub_start >= block_end:
                    new_blocks.append((block_start, block_end))
                elif sub_start <= block_start and sub_end >= block_end:
                    continue
                elif sub_start <= block_start:
                    new_blocks.append((sub_end, block_end))
                elif sub_end >= block_end:
                    new_blocks.append((block_start, sub_start))
                else:
                    new_blocks.extend([(block_start, sub_start), (sub_end, block_end)])
            current_blocks = new_blocks
        result.extend(current_blocks)
    return result


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


async def generate_availability_blocks(availabilities, start_date: datetime, end_date: datetime) -> List[
    Tuple[datetime, datetime]]:
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
            print(f"Failed to generate availability blocks: {str(e)}")
            continue
    return merge_overlapping_blocks(blocks)


def get_end_of_current_month() -> datetime:
    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    return datetime(today.year, today.month, last_day, 23, 59, 59, tzinfo=timezone.utc)