"""Metadata parsing helpers for project files."""

from datetime import date, datetime

from pydantic import JsonValue


def parse_date_or_datetime(value: JsonValue) -> date | datetime | None:
    """
    Parse the value as an ISO 8601 date or date/time.

    :param value: The value to parse.
    :return: The date or date/time, or None for invalid or missing values.
    """

    if not isinstance(value, str):
        return None

    try:
        return date.fromisoformat(value)
    except ValueError:
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None


def parse_date(value: JsonValue) -> date | None:
    """
    Parse the value as an ISO 8601 date.

    :param value: The value to parse.
    :return: The date, or None for invalid or missing values.
    """

    if not isinstance(value, str):
        return None

    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None


def parse_str(value: JsonValue) -> str | None:
    """
    Parse the value as a string.

    :param value: The value to parse.
    :return: The string, or None for invalid or missing values.
    """

    if isinstance(value, str):
        return value
    return None
