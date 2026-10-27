from datetime import date, datetime

import pytest
from pydantic import JsonValue

from preprocessor.core.serialization.metadata import parse_date, parse_date_or_datetime


class TestParseDateOrDatetime:
    """Tests for the parse_date_or_datetime() function."""

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("2025-08-27", date(2025, 8, 27)),
            ("2025-08-27T14:30:00", datetime(2025, 8, 27, 14, 30)),
        ],
    )
    def test_should_parse_iso_date_or_datetime_when_value_is_valid(
        self,
        value: JsonValue,
        expected: date | datetime,
    ) -> None:
        """Should parse a valid ISO date or date/time value."""

        # Arrange
        raw_value = value

        # Act
        parsed_value = parse_date_or_datetime(raw_value)

        # Assert
        assert parsed_value == expected

    @pytest.mark.parametrize("value", ["2025-02-30", "not a date", 2025, None])
    def test_should_return_none_when_iso_date_or_datetime_value_is_invalid(
        self,
        value: JsonValue,
    ) -> None:
        """Should return None for an invalid ISO date or date/time value."""

        # Arrange
        raw_value = value

        # Act
        parsed_value = parse_date_or_datetime(raw_value)

        # Assert
        assert parsed_value is None


class TestParseDate:
    """Tests for the parse_date() function."""

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("2025-08-27", date(2025, 8, 27)),
            ("2025-08-27T14:30:00", date(2025, 8, 27)),
        ],
    )
    def test_should_parse_iso_date_when_value_is_valid(
        self,
        value: JsonValue,
        expected: date,
    ) -> None:
        """Should parse the date from a valid ISO date or date/time value."""

        # Arrange
        raw_value = value

        # Act
        parsed_value = parse_date(raw_value)

        # Assert
        assert parsed_value == expected

    @pytest.mark.parametrize("value", ["2025-02-30", "not a date", 2025, None])
    def test_should_return_none_when_iso_date_value_is_invalid(
        self,
        value: JsonValue,
    ) -> None:
        """Should return None for an invalid ISO date value."""

        # Arrange
        raw_value = value

        # Act
        parsed_value = parse_date(raw_value)

        # Assert
        assert parsed_value is None
