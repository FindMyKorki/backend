import pytest
from datetime import datetime, timedelta, timezone
from app.tutors_availability.utils import (
    parse_recurrence_rule,
    get_weekday_num,
    generate_occurrences,
    subtract_time_blocks
)


class TestRecurrenceRuleParser:
    def test_empty_rule(self):
        """Test parsing an empty recurrence rule"""
        assert parse_recurrence_rule("") == {}
        assert parse_recurrence_rule(None) == {}

    def test_simple_rule(self):
        """Test parsing a basic recurrence rule"""
        rule = "FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,WE,FR"
        parsed = parse_recurrence_rule(rule)
        
        assert parsed["FREQ"] == "WEEKLY"
        assert parsed["INTERVAL"] == 1
        assert parsed["BYDAY"] == ["MO", "WE", "FR"]

    def test_rule_with_until(self):
        """Test parsing a rule with end date"""
        rule = "FREQ=DAILY;UNTIL=20251231"
        parsed = parse_recurrence_rule(rule)
        
        assert parsed["FREQ"] == "DAILY"
        assert parsed["UNTIL"] == "20251231"

    def test_monthly_rule(self):
        """Test parsing a monthly recurrence rule"""
        rule = "FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=15"
        parsed = parse_recurrence_rule(rule)
        
        assert parsed["FREQ"] == "MONTHLY"
        assert parsed["INTERVAL"] == 2
        assert parsed["BYMONTHDAY"] == ["15"]


class TestWeekdayConverter:
    def test_weekday_conversion(self):
        """Test converting weekday codes to numbers"""
        assert get_weekday_num("MO") == 0
        assert get_weekday_num("TU") == 1
        assert get_weekday_num("WE") == 2
        assert get_weekday_num("TH") == 3
        assert get_weekday_num("FR") == 4
        assert get_weekday_num("SA") == 5
        assert get_weekday_num("SU") == 6
        
    def test_invalid_weekday(self):
        """Test converting an invalid weekday code"""
        assert get_weekday_num("INVALID") == 0
        assert get_weekday_num("") == 0


class TestOccurrenceGenerator:
    def test_one_time_occurrence(self):
        """Test generating a one-time occurrence without recurrence rule"""
        start_date = datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc)
        end_date = datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc)
        query_start = datetime(2025, 3, 1, tzinfo=timezone.utc)
        query_end = datetime(2025, 4, 1, tzinfo=timezone.utc)
        
        occurrences = generate_occurrences(start_date, end_date, "", query_start, query_end)
        
        assert len(occurrences) == 1
        assert occurrences[0][0] == start_date
        assert occurrences[0][1] == end_date
    
    def test_one_time_occurrence_outside_range(self):
        """Test occurrence outside query range is not included"""
        start_date = datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc)
        end_date = datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc)
        query_start = datetime(2025, 4, 1, tzinfo=timezone.utc)
        query_end = datetime(2025, 4, 30, tzinfo=timezone.utc)
        
        occurrences = generate_occurrences(start_date, end_date, "", query_start, query_end)
        
        assert len(occurrences) == 0
    
    def test_daily_occurrences(self):
        """Test generating daily occurrences"""
        start_date = datetime(2025, 3, 1, 10, 0, tzinfo=timezone.utc)
        end_date = datetime(2025, 3, 1, 12, 0, tzinfo=timezone.utc)
        rule = "FREQ=DAILY;INTERVAL=1"
        query_start = datetime(2025, 3, 1, tzinfo=timezone.utc)
        query_end = datetime(2025, 3, 5, tzinfo=timezone.utc)
        
        occurrences = generate_occurrences(start_date, end_date, rule, query_start, query_end)
        
        assert len(occurrences) == 5
        
        assert occurrences[0][0] == datetime(2025, 3, 1, 10, 0, tzinfo=timezone.utc)
        assert occurrences[0][1] == datetime(2025, 3, 1, 12, 0, tzinfo=timezone.utc)
        assert occurrences[-1][0] == datetime(2025, 3, 5, 10, 0, tzinfo=timezone.utc)
        assert occurrences[-1][1] == datetime(2025, 3, 5, 12, 0, tzinfo=timezone.utc)
    
    def test_weekly_occurrences_with_specific_days(self):
        """Test generating weekly occurrences for specific days"""
        start_date = datetime(2025, 3, 3, 16, 0, tzinfo=timezone.utc)
        end_date = datetime(2025, 3, 3, 18, 0, tzinfo=timezone.utc)
        rule = "FREQ=WEEKLY;BYDAY=MO,WE,FR"
        query_start = datetime(2025, 3, 1, tzinfo=timezone.utc)
        query_end = datetime(2025, 3, 31, tzinfo=timezone.utc)
        
        occurrences = generate_occurrences(start_date, end_date, rule, query_start, query_end)
        
        assert len(occurrences) == 13
        
        for start, end in occurrences:
            weekday = start.weekday()
            assert weekday in [0, 2, 4]
            
            assert end - start == timedelta(hours=2)
    
    def test_monthly_occurrences(self):
        """Test generating monthly occurrences"""
        start_date = datetime(2025, 1, 15, 14, 0, tzinfo=timezone.utc)
        end_date = datetime(2025, 1, 15, 16, 0, tzinfo=timezone.utc)
        rule = "FREQ=MONTHLY;BYMONTHDAY=15"
        query_start = datetime(2025, 1, 1, tzinfo=timezone.utc)
        query_end = datetime(2025, 6, 30, tzinfo=timezone.utc)
        
        occurrences = generate_occurrences(start_date, end_date, rule, query_start, query_end)
        
        assert len(occurrences) == 6
        
        for start, end in occurrences:
            assert start.day == 15
            
            assert end - start == timedelta(hours=2)
    
    def test_with_until_date(self):
        """Test generating occurrences with an until date in the rule"""
        start_date = datetime(2025, 3, 1, 10, 0, tzinfo=timezone.utc)
        end_date = datetime(2025, 3, 1, 12, 0, tzinfo=timezone.utc)
        rule = "FREQ=DAILY;UNTIL=20250315"
        query_start = datetime(2025, 3, 1, tzinfo=timezone.utc)
        query_end = datetime(2025, 3, 31, tzinfo=timezone.utc)
        
        occurrences = generate_occurrences(start_date, end_date, rule, query_start, query_end)
        
        assert len(occurrences) == 15
        
        assert occurrences[-1][0] == datetime(2025, 3, 15, 10, 0, tzinfo=timezone.utc)


class TestTimeBlockSubtraction:
    def test_block_in_middle(self):
        """Test subtracting a block in the middle of another block"""
        base_blocks = [(datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc))]
        subtract_blocks = [(datetime(2025, 3, 28, 18, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 19, 0, tzinfo=timezone.utc))]
        
        result = subtract_time_blocks(base_blocks, subtract_blocks)
        
        assert len(result) == 2
        assert result[0] == (datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 18, 0, tzinfo=timezone.utc))
        assert result[1] == (datetime(2025, 3, 28, 19, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc))
    
    def test_block_at_start(self):
        """Test subtracting a block at the start of another block"""
        base_blocks = [(datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc))]
        subtract_blocks = [(datetime(2025, 3, 28, 15, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 18, 0, tzinfo=timezone.utc))]
        
        result = subtract_time_blocks(base_blocks, subtract_blocks)
        
        assert len(result) == 1
        assert result[0] == (datetime(2025, 3, 28, 18, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc))
    
    def test_block_at_end(self):
        """Test subtracting a block at the end of another block"""
        base_blocks = [(datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc))]
        subtract_blocks = [(datetime(2025, 3, 28, 18, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 21, 0, tzinfo=timezone.utc))]
        
        result = subtract_time_blocks(base_blocks, subtract_blocks)
        
        assert len(result) == 1
        assert result[0] == (datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 18, 0, tzinfo=timezone.utc))
    
    def test_complete_overlap(self):
        """Test subtracting a block that completely overlaps another block"""
        base_blocks = [(datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc))]
        subtract_blocks = [(datetime(2025, 3, 28, 15, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 21, 0, tzinfo=timezone.utc))]
        
        result = subtract_time_blocks(base_blocks, subtract_blocks)
        
        assert len(result) == 0
    
    def test_no_overlap(self):
        """Test subtracting a block that doesn't overlap"""
        base_blocks = [(datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc))]
        subtract_blocks = [(datetime(2025, 3, 28, 21, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 22, 0, tzinfo=timezone.utc))]
        
        result = subtract_time_blocks(base_blocks, subtract_blocks)
        
        assert len(result) == 1
        assert result[0] == (datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc))
    
    def test_day_long_availability_with_unavailability(self):
        """Test specifically to debug the problem with availabilities and unavailabilities handling difference"""
        # Availability spanning whole day
        base_blocks = [(
            datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), 
            datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc)
        )]
        
        # Unavailability in the middle of the day (13:00-14:00)
        subtract_blocks = [(
            datetime(2025, 4, 10, 13, 0, tzinfo=timezone.utc), 
            datetime(2025, 4, 10, 14, 0, tzinfo=timezone.utc)
        )]
        
        result = subtract_time_blocks(base_blocks, subtract_blocks)
        
        # Should result in two blocks: 10:00-13:00 and 14:00-18:00
        assert len(result) == 2
        assert result[0] == (datetime(2025, 4, 10, 10, 0, tzinfo=timezone.utc), datetime(2025, 4, 10, 13, 0, tzinfo=timezone.utc))
        assert result[1] == (datetime(2025, 4, 10, 14, 0, tzinfo=timezone.utc), datetime(2025, 4, 10, 18, 0, tzinfo=timezone.utc))
    
    def test_multiple_subtractions(self):
        """Test subtracting multiple blocks from one block"""
        base_blocks = [(datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc))]
        subtract_blocks = [
            (datetime(2025, 3, 28, 17, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 18, 0, tzinfo=timezone.utc)),
            (datetime(2025, 3, 28, 19, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 19, 30, tzinfo=timezone.utc))
        ]
        
        result = subtract_time_blocks(base_blocks, subtract_blocks)
        
        assert len(result) == 3
        assert result[0] == (datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 17, 0, tzinfo=timezone.utc))
        assert result[1] == (datetime(2025, 3, 28, 18, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 19, 0, tzinfo=timezone.utc))
        assert result[2] == (datetime(2025, 3, 28, 19, 30, tzinfo=timezone.utc), datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc))
    
    def test_multiple_base_blocks(self):
        """Test subtracting a block from multiple base blocks"""
        base_blocks = [
            (datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 18, 0, tzinfo=timezone.utc)),
            (datetime(2025, 3, 28, 19, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 21, 0, tzinfo=timezone.utc))
        ]
        subtract_blocks = [(datetime(2025, 3, 28, 17, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc))]
        
        result = subtract_time_blocks(base_blocks, subtract_blocks)
        
        assert len(result) == 2
        assert result[0] == (datetime(2025, 3, 28, 16, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 17, 0, tzinfo=timezone.utc))
        assert result[1] == (datetime(2025, 3, 28, 20, 0, tzinfo=timezone.utc), datetime(2025, 3, 28, 21, 0, tzinfo=timezone.utc)) 