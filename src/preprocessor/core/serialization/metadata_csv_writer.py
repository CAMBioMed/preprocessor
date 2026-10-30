"""CSV serialization for photo metadata."""

from __future__ import annotations

import csv
from collections.abc import Mapping
from datetime import date
from typing import TextIO

from pydantic import JsonValue

from preprocessor.core.serialization.metadata import parse_date


class MetadataCsvWriter:
    """Write photo metadata using the project's metadata CSV format."""

    _HEADERS = (
        "Name",
        "Date",
        "Partner",
        "Area",
        "Site",
        "Season",
        "Transect",
        "Height (cm)",
        "Latitude",
        "Longitude",
        "Depth",
        "Camera",
        "Photographer",
        "Water quality",
        "Strobes",
        "Framing gear used",
        "White balance card",
        "Comments",
    )

    def __init__(self, file: TextIO) -> None:
        """Create a writer and write the CSV header to ``file``.

        :param file: A text stream receiving CSV output.
        """

        self._writer = csv.writer(file, dialect="excel")
        self._writer.writerow(self.csv_headers())

    @staticmethod
    def csv_headers() -> list[str]:
        """Return the CSV headers for the metadata fields."""

        return list(MetadataCsvWriter._HEADERS)

    def write_row(self, metadata: Mapping[str, JsonValue]) -> None:
        """Write one metadata mapping as a CSV row.

        Unknown metadata fields are ignored. String values are trimmed and
        blank strings are written as empty values, matching the legacy
        metadata CSV behavior.

        :param metadata: Metadata values for one photo.
        """

        self._writer.writerow(self.csv_row(metadata))

    @staticmethod
    def csv_row(metadata: Mapping[str, JsonValue]) -> list[str]:
        """Convert one metadata mapping to the legacy CSV row format."""

        metadata_date = metadata.get("date")
        parsed_date: date | None = parse_date(metadata_date.strip()) if isinstance(metadata_date, str) else None

        return [
            MetadataCsvWriter._text(metadata.get("filename")),
            parsed_date.isoformat() if parsed_date else "",
            MetadataCsvWriter._text(metadata.get("partner")),
            MetadataCsvWriter._text(metadata.get("area")),
            MetadataCsvWriter._text(metadata.get("site")),
            MetadataCsvWriter._text(metadata.get("season")),
            MetadataCsvWriter._text(metadata.get("transect")),
            MetadataCsvWriter._value(metadata.get("height")),
            MetadataCsvWriter._value(metadata.get("latitude")),
            MetadataCsvWriter._value(metadata.get("longitude")),
            MetadataCsvWriter._text(metadata.get("depth")),
            MetadataCsvWriter._text(metadata.get("camera")),
            MetadataCsvWriter._text(metadata.get("photographer")),
            MetadataCsvWriter._text(metadata.get("water_quality")),
            MetadataCsvWriter._text(metadata.get("strobes")),
            MetadataCsvWriter._text(metadata.get("framing")),
            MetadataCsvWriter._text(metadata.get("white_balance_card")),
            MetadataCsvWriter._text(metadata.get("comments")),
        ]

    @staticmethod
    def _text(value: JsonValue) -> str:
        if not isinstance(value, str):
            return ""
        return value.strip()

    @staticmethod
    def _value(value: JsonValue) -> str:
        if isinstance(value, str):
            return value.strip()
        return "" if value is None else str(value)
