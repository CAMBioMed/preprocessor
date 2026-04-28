from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import ClassVar, override

import pytest

from preprocessor.core.model import MetadataData

from tests.preprocessor.core.model.cls_PydanticModelTestBase import PydanticModelTestBase


class Test_MetadataData(PydanticModelTestBase):

    fields_and_values: ClassVar[dict[str, tuple[
        object | None,
        list[object],
        list[tuple[object, object]],
        list[object],
    ]]] = {
        "filename": (
            # Initial
            None,
            # Valid
            [
                "Test-Name.jpg",
                "x" * 200,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  Other-Name.jpg  ", "Other-Name.jpg"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 201,  # Must be <= 200 chars
            ],
        ),
        "date": (
            # Initial
            None,
            # Valid
            [
                datetime(2026, 3, 24, 14, 0, 0),
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("2016-05-30", datetime(2016, 5, 30, 0, 0, 0)),
                ("2016-05-30T15:46:24", datetime(2016, 5, 30, 15, 46, 24)),
                (
                    "2025-09-20T16:35:48.429000+02:00",
                    datetime(2025, 9, 20, 16, 35, 48, 429000, tzinfo=timezone(timedelta(seconds=7200))),
                ),
                (
                    "2025-05-04T13:17:58+01:00",
                    datetime(2025, 5, 4, 13, 17, 58, tzinfo=timezone(timedelta(seconds=3600))),
                ),
                ("2025-12-15T10:30:00Z", datetime(2025, 12, 15, 10, 30, 0, tzinfo=timezone.utc)),
                ("  2026-04-26T14:00:00  ", datetime(2026, 4, 26, 14, 0, 0)),  # Trims whitespace
            ],
            # Invalid
            [
                "not a date",  # Invalid type
            ],
        ),
        "partner": (
            # Initial
            None,
            # Valid
            [
                "Acme Corp",
                "x" * 50,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  A113  ", "A113"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 51,  # Must be <= 50 chars
            ],
        ),
        "area": (
            # Initial
            None,
            # Valid
            [
                "Coral Reef",
                "x" * 50,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  Coral Bay  ", "Coral Bay"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 51,  # Must be <= 50 chars
            ],
        ),
        "site": (
            # Initial
            None,
            # Valid
            [
                "Isla Nublar",
                "x" * 50,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  Isla Sorna  ", "Isla Sorna"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 51  # Must be <= 50 chars
            ],
        ),
        "season": (
            # Initial
            None,
            # Valid
            [
                "Spring",
                "x" * 50,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  Summer  ", "Summer"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 51  # Must be <= 50 chars
            ],
        ),
        "transect": (
            # Initial
            None,
            # Valid
            [
                "Transect 1",
                "x" * 50,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  T2  ", "T2"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 51  # Must be <= 50 chars
            ],
        ),
        "height": (
            # Initial
            None,
            # Valid
            [
                10000,
                0,
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" 10 ", 10),  # Trims whitespace and converts to int
            ],
            # Invalid
            [
                "not a number",  # Invalid type
                -100,  # Must be >= 0
            ],
        ),
        "latitude": (
            # Initial
            None,
            # Valid
            [
                34.0522,
                -90.0,
                90.0,
                0.0,
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" 45.03 ", 45.03),  # Trims whitespace and converts to float
            ],
            # Invalid
            [
                "not a number",  # Invalid type
                100.0,  # Must be <= 90
                -100.0,  # Must be >= -90
            ],
        ),
        "longitude": (
            # Initial
            None,
            # Valid
            [
                -118.2437,
                -180.0,
                180.0,
                0.0,
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" -109.25 ", -109.25),  # Trims whitespace and converts to float
            ],
            # Invalid
            [
                "not a number",  # Invalid type
                200.0,  # Must be <= 180
                -200.0,  # Must be >= -180
            ],
        ),
        "depth": (
            # Initial
            None,
            # Valid
            [
                "20m",
                "x" * 45,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" 25m ", "25m"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 46,  # Must be <= 45 chars
            ],
        ),
        "camera": (
            # Initial
            None,
            # Valid
            [
                "Canon EOS R5",
                "x" * 200,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" Nikon D7000 ", "Nikon D7000"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 201,  # Must be <= 200 chars
            ],
        ),
        "photographer": (
            # Initial
            None,
            # Valid
            [
                "Jane Doe",
                "x" * 45,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" John Cleese ", "John Cleese"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 46,  # Must be <= 45 chars
            ],
        ),
        "water_quality": (
            # Initial
            None,
            # Valid
            [
                "Clear",
                "x" * 45,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" Troubled ", "Troubled"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 46,  # Must be <= 45 chars
            ],
        ),
        "strobes": (
            # Initial
            None,
            # Valid
            [
                "Yes",
                "x" * 200,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" No ", "No"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 201,  # Must be <= 200 chars
            ],
        ),
        "framing": (
            # Initial
            None,
            # Valid
            [
                "Tight",
                "x" * 200,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" Wide ", "Wide"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 201,  # Must be <= 200 chars
            ],
        ),
        "white_balance_card": (
            # Initial
            None,
            # Valid
            [
                "Yes",
                "x" * 200,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" No ", "No"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 201,  # Must be <= 200 chars
            ],
        ),
        "comments": (
            # Initial
            None,
            # Valid
            [
                "No issues",
                "x" * 1000,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" Many issues ", "Many issues"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 1001,  # Must be <= 1000 chars
            ],
        ),
    }
    """Map for each field name to:
    - the default value,
    - a list of valid values,
    - a list of pairs: unnormalized value to normalized value,
    - a list of invalid values
    """

    @override
    def create_model(self) -> MetadataData:
        return MetadataData()

    @override
    def update_model(self, model: MetadataData, field_name: str, new_value: object) -> MetadataData:
        setattr(model, field_name, new_value)
        return model


    @pytest.mark.parametrize(
        "field_name, initial_value, new_value",
        [(n, v, vv) for n, (v, vvs, _, _) in fields_and_values.items() for vv in vvs],
    )
    def test_property_valid_value(
        self,
        field_name: str,
        initial_value: object,
        new_value: object,
    ) -> None:
        self.assert_property_valid_value(field_name, initial_value, new_value)

    @pytest.mark.parametrize(
        "field_name, initial_value, invalid_value",
        [(n, v, iv) for n, (v, _, _, ivs) in fields_and_values.items() for iv in ivs],
    )
    def test_property_invalid_value(
        self,
        field_name: str,
        initial_value: object,
        invalid_value: object,
    ) -> None:
        self.assert_property_invalid_value(field_name, initial_value, invalid_value)

    @pytest.mark.parametrize(
        "field_name, initial_value, input_value, expected_value",
        [(n, v, lv, rv) for n, (v, _, nvs, _) in fields_and_values.items() for (lv, rv) in nvs],
    )
    def test_property_normalization(
        self,
        field_name: str,
        initial_value: object,
        input_value: object,
        expected_value: object,
    ) -> None:
        self.assert_property_normalization(field_name, initial_value, input_value, expected_value)
