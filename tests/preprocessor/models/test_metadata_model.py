from datetime import datetime, date, timezone, timedelta
from typing import cast

import pytest
from pytestqt.qtbot import QtBot

from preprocessor.model.metadata_model import MetadataModel, MetadataData
from tests.preprocessor.models.qmodel_fixture import (
    assert_model_property_getter_setter_and_signal,
    assert_has_a_property_for_each_data_field,
)


class TestMetadataModel:
    """Unit tests for MetadataModel and MetadataData."""

    fields_and_values: dict[str, tuple[object | None, list[object], list[tuple[object, object]], list[object]]] = {
        "filename": (None, [
            "Test-Name.jpg",
            "x" * 200,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            ("  Test-Name.jpg  ", "Test-Name.jpg"),  # Trims whitespace
        ], [
            "x" * 201,  # Must be <= 200 chars
        ]),
        "date": (None, [
            datetime(2026, 3, 24, 14, 0, 0),
        ], [
            ("", None),  # Empty string becomes None
            ("2016-05-30", datetime(2016, 5, 30, 0, 0, 0)),
            ("2016-05-30T15:46:24", datetime(2016, 5, 30, 15, 46, 24)),
            ("2025-09-20T16:35:48.429000+02:00", datetime(2025, 9, 20, 16, 35, 48, 429000, tzinfo=timezone(timedelta(seconds=7200)))),
            ("2025-05-04T13:17:58+01:00", datetime(2025, 5, 4, 13, 17, 58, tzinfo=timezone(timedelta(seconds=3600)))),
            ("2025-12-15T10:30:00Z", datetime(2025, 12, 15, 10, 30, 0, tzinfo=timezone.utc)),
            ("  2026-03-24T14:00:00  ", datetime(2026, 3, 24, 14, 0, 0)),  # Trims whitespace
        ], [
            "not a date",  # Invalid type
        ]),
        "partner": (None, [
            "Acme Corp",
            "x" * 50,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            ("  Acme Corp  ", "Acme Corp"),  # Trims whitespace
        ], [
            "x" * 51,  # Must be <= 50 chars
        ]),
        "area": (None, [
            "Coral Reef",
            "x" * 50,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            ("  Coral Reef  ", "Coral Reef"),  # Trims whitespace
        ], [
            "x" * 51,  # Must be <= 50 chars
        ]),
        "site": (None, [
            "Site A",
            "x" * 50,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            ("  Site A  ", "Site A"),  # Trims whitespace
        ], [
            "x" * 51  # Must be <= 50 chars
        ]),
        "season": (None, [
            "Spring",
            "x" * 50,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            ("  Spring  ", "Spring"),  # Trims whitespace
        ], [
            "x" * 51  # Must be <= 50 chars
        ]),
        "transect": (None, [
            "Transect 1",
            "x" * 50,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            ("  Transect 1  ", "Transect 1"),  # Trims whitespace
        ], [
            "x" * 51  # Must be <= 50 chars
        ]),
        "height": (None, [
            10000,
            0,
        ], [
            ("", None),  # Empty string becomes None
            (" 10 ", 10),  # Trims whitespace and converts to int
        ], [
            "not a number",  # Invalid type
            -100,  # Must be >= 0
        ]),
        "latitude": (None, [
            34.0522,
            -90.0,
            90.0,
            0.0,
        ], [
            ("", None),  # Empty string becomes None
            (" 34.0522 ", 34.0522),  # Trims whitespace and converts to float
        ], [
            "not a number",  # Invalid type
            100.0,  # Must be <= 90
            -100.0,  # Must be >= -90
        ]),
        "longitude": (None, [
            -118.2437,
            -180.0,
            180.0,
            0.0,
        ], [
            ("", None),  # Empty string becomes None
            (" -118.2437 ", -118.2437),  # Trims whitespace and converts to float
        ], [
            "not a number",  # Invalid type
            200.0,  # Must be <= 180
            -200.0,  # Must be >= -180
        ]),
        "depth": (None, [
            "20m",
            "x" * 45,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            (" 20m ", "20m"),  # Trims whitespace
        ], [
            "x" * 46,  # Must be <= 45 chars
        ]),
        "camera": (None, [
            "Canon EOS R5",
            "x" * 200,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            (" Canon EOS R5 ", "Canon EOS R5"),  # Trims whitespace
        ], [
            "x" * 201,  # Must be <= 200 chars
        ]),
        "photographer": (None, [
            "Jane Doe",
            "x" * 45,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            (" Jane Doe ", "Jane Doe"),  # Trims whitespace
        ], [
            "x" * 46,  # Must be <= 45 chars
        ]),
        "water_quality": (None, [
            "Clear",
            "x" * 45,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            (" Clear ", "Clear"),  # Trims whitespace
        ], [
            "x" * 46,  # Must be <= 45 chars
        ]),
        "strobes": (None, [
            "Yes",
            "x" * 200,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            (" Yes ", "Yes"),  # Trims whitespace
        ], [
            "x" * 201,  # Must be <= 200 chars
        ]),
        "framing": (None, [
            "Tight",
            "x" * 200,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            (" Tight ", "Tight"),  # Trims whitespace
        ], [
            "x" * 201,  # Must be <= 200 chars
        ]),
        "white_balance_card": (None, [
            "Yes",
            "x" * 200,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            (" Yes ", "Yes"),  # Trims whitespace
        ], [
            "x" * 201,  # Must be <= 200 chars
        ]),
        "comments": (None, [
            "No issues",
            "x" * 1000,  # Max length
        ], [
            ("", None),  # Empty string becomes None
            (" No issues ", "No issues"),  # Trims whitespace
        ], [
            "x" * 1001,  # Must be <= 1000 chars
        ]),
    }
    """Map for each field name to:
    - the default value,
    - a list of valid values,
    - a list of pairs: unnormalized value to normalized value,
    - a list of invalid values
    """

    def test_has_a_property_for_each_data_field(self) -> None:
        """Model should have a property for each field in the data model."""
        assert_has_a_property_for_each_data_field(MetadataModel, MetadataData)

    fields_name_initial_new = [
        (field_name, initial_value, valid_value)
        for field_name, (initial_value, valid_values, _, _) in fields_and_values.items()
        for valid_value in valid_values
    ]

    @pytest.mark.parametrize("field_name, initial_value, new_value", fields_name_initial_new)
    def test_properties_getter_setter_and_signals(
        self, qtbot: QtBot, field_name: str, initial_value: object, new_value: object
    ) -> None:
        """Model properties should have working getters, setters, and change signals."""
        with qtbot.capture_exceptions():
            # Arrange: empty MetadataModel
            model = MetadataModel()

            # Assert: fields signal correctly on change
            assert_model_property_getter_setter_and_signal(qtbot, model, field_name, initial_value, new_value)

    fields_name_invalid = [
        (field_name, invalid_value)
        for field_name, (initial_value, _, _, invalid_values) in fields_and_values.items()
        for invalid_value in invalid_values
    ]

    @pytest.mark.parametrize("field_name, invalid_value", fields_name_invalid)
    def test_properties_validation(self, field_name: str, invalid_value: object) -> None:
        """Model properties should enforce type validation and constraints when set."""
        model = MetadataModel()

        with pytest.raises(ValueError):
            setattr(model, field_name, invalid_value)

    fields_name_value_normalized = [
        (field_name, left, right)
        for field_name, (initial_value, _, normalized_pairs, _) in fields_and_values.items()
        for (left, right) in normalized_pairs
    ]

    @pytest.mark.parametrize("field_name, input_value, expected_value", fields_name_value_normalized)
    def test_properties_normalization(self, field_name: str, input_value: object, expected_value: object) -> None:
        """Model properties should normalize (trimming, empty to None) on assignment."""
        model = MetadataModel()

        # Act: set the value
        setattr(model, field_name, input_value)

        # Assert: the value is normalized as expected
        assert getattr(model, field_name) == expected_value
