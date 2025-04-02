from datetime import datetime, timedelta, timezone
from typing import List, Tuple
import re


def standardize_datetime(dt: datetime) -> datetime:
    """
    Ensures a datetime object has timezone information.
    If the datetime is naive (has no timezone), it assigns UTC timezone.
    
    Args:
        dt: A datetime object which may or may not have timezone info
        
    Returns:
        A datetime object with timezone information (aware datetime)
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def parse_recurrence_rule(rule: str) -> dict:
    """
    Parses recurrence rule into a dictionary
    
    Rule format can be e.g. FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,WE,FR
    where:
    - FREQ defines frequency (DAILY, WEEKLY, MONTHLY, YEARLY)
    - INTERVAL defines repetition interval (e.g. every 1 week, every 2 weeks)
    - BYDAY defines weekdays (MO, TU, WE, TH, FR, SA, SU)
    - BYMONTHDAY defines days of month (1-31)
    - BYMONTH defines months (1-12)
    """
    if not rule:
        return {}
    
    result = {}
    parts = rule.split(';')
    
    for part in parts:
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
    """Converts weekday code to number (0-6)"""
    days = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}
    return days.get(day_code, 0)


def generate_occurrences(start_date: datetime, end_date: datetime, 
                         recurrence_rule: str, query_start: datetime, query_end: datetime) -> List[Tuple[datetime, datetime]]:
    """
    Generates all occurrences of an event based on start date, 
    end date and recurrence rule, within the specified query range
    
    Args:
        start_date: Event start date
        end_date: Event end date
        recurrence_rule: Recurrence rule
        query_start: Query range start date
        query_end: Query range end date (inclusive)
        
    Returns:
        List of tuples (start_date, end_date) for each occurrence
    """
    result = []
    
    start_date = standardize_datetime(start_date)
    end_date = standardize_datetime(end_date)
    query_start = standardize_datetime(query_start)
    query_end = standardize_datetime(query_end)
    
    if not recurrence_rule:
        if (start_date <= query_end and end_date >= query_start):
            result.append((start_date, end_date))
        return result
    
    rule_dict = parse_recurrence_rule(recurrence_rule)
    
    freq = rule_dict.get('FREQ')
    interval = rule_dict.get('INTERVAL', 1)
    
    effective_query_end = datetime(
        query_end.year, query_end.month, query_end.day, 23, 59, 59, 999999, tzinfo=query_end.tzinfo
    )
    
    rule_until = None
    if 'UNTIL' in rule_dict:
        until_date_str = rule_dict['UNTIL']
        if len(until_date_str) >= 8:
            year = int(until_date_str[0:4])
            month = int(until_date_str[4:6])
            day = int(until_date_str[6:8])
            rule_until = datetime(year, month, day, 23, 59, 59, tzinfo=timezone.utc)
    
    until_date = effective_query_end
    if rule_until is not None:
        until_date = min(until_date, rule_until)
    
    duration = end_date - start_date
    
    if freq == 'DAILY':
        current_date = start_date
        
        if current_date < query_start:
            days_to_add = (query_start - current_date).days
            days_to_add = (days_to_add // interval) * interval
            if days_to_add > 0:
                current_date = current_date + timedelta(days=days_to_add)
        
        while current_date <= until_date:
            event_end = current_date + duration
            
            if current_date <= until_date and event_end >= query_start:
                result.append((current_date, event_end))
            
            current_date = current_date + timedelta(days=interval)
    
    elif freq == 'WEEKLY':
        weekdays_to_include = None
        if 'BYDAY' in rule_dict:
            weekdays_to_include = [get_weekday_num(day) for day in rule_dict['BYDAY']]
        else:
            weekdays_to_include = [start_date.weekday()]
        
        base_date = start_date
        
        if base_date < query_start:
            days_to_add = (query_start - base_date).days
            weeks_to_add = days_to_add // 7
            weeks_to_add = (weeks_to_add // interval) * interval
            if weeks_to_add > 0:
                base_date = base_date + timedelta(days=weeks_to_add * 7)
        
        current_week_start = base_date - timedelta(days=base_date.weekday())
        
        while current_week_start <= until_date:
            for weekday in weekdays_to_include:
                current_date = current_week_start + timedelta(days=weekday)
                
                current_date = current_date.replace(
                    hour=base_date.hour,
                    minute=base_date.minute,
                    second=base_date.second,
                    microsecond=base_date.microsecond
                )
                
                event_end = current_date + duration
                
                if (current_date <= until_date and event_end >= query_start):
                    result.append((current_date, event_end))
            
            current_week_start = current_week_start + timedelta(days=7 * interval)
    
    elif freq == 'MONTHLY':
        current_date = start_date
        
        if current_date < query_start:
            months_diff = (query_start.year - current_date.year) * 12 + query_start.month - current_date.month
            months_to_add = (months_diff // interval) * interval
            
            if months_to_add > 0:
                new_month = ((current_date.month - 1 + months_to_add) % 12) + 1
                new_year = current_date.year + (current_date.month - 1 + months_to_add) // 12
                
                max_day = 31
                if new_month in [4, 6, 9, 11]:
                    max_day = 30
                elif new_month == 2:
                    if (new_year % 4 == 0 and (new_year % 100 != 0 or new_year % 400 == 0)):
                        max_day = 29
                    else:
                        max_day = 28
                
                new_day = min(current_date.day, max_day)
                
                current_date = current_date.replace(year=new_year, month=new_month, day=new_day)
        
        while current_date <= until_date:
            monthday_match = True
            if 'BYMONTHDAY' in rule_dict:
                monthday_match = str(current_date.day) in rule_dict['BYMONTHDAY']
            
            month_match = True
            if 'BYMONTH' in rule_dict:
                month_match = str(current_date.month) in rule_dict['BYMONTH']
            
            if monthday_match and month_match:
                event_end = current_date + duration
                
                if current_date <= until_date and event_end >= query_start:
                    result.append((current_date, event_end))
            
            month = current_date.month - 1 + interval
            year = current_date.year + month // 12
            month = month % 12 + 1
            
            max_day = 31
            if month in [4, 6, 9, 11]:
                max_day = 30
            elif month == 2:
                if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
                    max_day = 29
                else:
                    max_day = 28
            
            day = min(current_date.day, max_day)
            
            try:
                current_date = current_date.replace(year=year, month=month, day=day)
            except ValueError:
                last_day = max_day
                current_date = current_date.replace(year=year, month=month, day=last_day)
    
    return result


def subtract_time_blocks(base_blocks: List[Tuple[datetime, datetime]], 
                         subtract_blocks: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:
    """
    Subtracts a list of time blocks from another list of blocks
    
    Args:
        base_blocks: List of base time blocks (start, end)
        subtract_blocks: List of blocks to subtract (start, end)
        
    Returns:
        List of time blocks after subtraction
    """
    result = []
    
    for base_start, base_end in base_blocks:
        current_blocks = [(base_start, base_end)]
        new_blocks = []
        
        for sub_start, sub_end in subtract_blocks:
            for block_start, block_end in current_blocks:
                if sub_end <= block_start or sub_start >= block_end:
                    new_blocks.append((block_start, block_end))
                elif sub_start <= block_start and sub_end >= block_end:
                    pass
                elif sub_start <= block_start and sub_end > block_start and sub_end < block_end:
                    new_blocks.append((sub_end, block_end))
                elif sub_start > block_start and sub_start < block_end and sub_end >= block_end:
                    new_blocks.append((block_start, sub_start))
                elif sub_start > block_start and sub_end < block_end:
                    new_blocks.append((block_start, sub_start))
                    new_blocks.append((sub_end, block_end))
            
            current_blocks = new_blocks
            new_blocks = []
        
        result.extend(current_blocks)
    
    return result 