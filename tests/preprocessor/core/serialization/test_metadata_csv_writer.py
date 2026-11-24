from __future__ import annotations

import csv
from io import StringIO

from pydantic import JsonValue

from preprocessor.core.serialization import MetadataCsvWriter


def test_should_match_metadata_data_csv_output_when_metadata_is_written() -> None:
    """Should match MetadataData CSV output when metadata is written."""

    # Arrange
    output = StringIO(newline="")
    writer = MetadataCsvWriter(output)
    metadata: dict[str, JsonValue] = {
        "filename": "  testfile.jpg  ",
        "date": " 2023-09-01T12:00:00Z ",
        "partner": " SZN ",
        "area": "Crete",
        "site": "Site1",
        "season": "Fall",
        "transect": "Transect1",
        "height": " 100 ",
        "latitude": " 35.0 ",
        "longitude": 25.0,
        "depth": "10m",
        "camera": "Nikon D850",
        "photographer": "John Doe",
        "water_quality": "Clear",
        "strobes": "Strobe1",
        "framing": "Framing1",
        "white_balance_card": "Card1",
        "comments": "No comments",
        "unsupported": "ignored",
    }

    # Act
    writer.write_row(metadata)

    # Assert
    rows = list(csv.reader(StringIO(output.getvalue())))
    assert rows == [
        [
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
        ],
        [
            "testfile.jpg",
            "2023-09-01",
            "SZN",
            "Crete",
            "Site1",
            "Fall",
            "Transect1",
            "100",
            "35.0",
            "25.0",
            "10m",
            "Nikon D850",
            "John Doe",
            "Clear",
            "Strobe1",
            "Framing1",
            "Card1",
            "No comments",
        ],
    ]
