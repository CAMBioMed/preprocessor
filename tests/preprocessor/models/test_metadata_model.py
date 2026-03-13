from datetime import datetime, date
from typing import cast

import pytest
from pytestqt.qtbot import QtBot

from preprocessor.model.metadata_model import MetadataModel, MetadataData
from tests.preprocessor.models.qmodel_fixture import assert_model_property_getter_setter_and_signal, \
    assert_has_a_property_for_each_data_field


class TestMetadataModel:
    """Unit tests for MetadataModel and MetadataData."""

    def test_has_a_property_for_each_data_field(self) -> None:
        """Model should have a property for each field in the data model."""
        assert_has_a_property_for_each_data_field(MetadataModel, MetadataData)

    fields_name_initial_new = [
        ("date", None, datetime(2026, 3, 24, 14, 0, 0)),
        ("partner", None, "Acme Corp"),
        ("area", None, "Coral Reef"),
        ("site", None, "Site A"),
        ("season", None, "Spring"),
        ("transect", None, "Transect 1"),
        ("height", None, "10m"),
        ("latitude", None, 34.0522),
        ("longitude", None, -118.2437),
        ("depth", None, "20m"),
        ("camera", None, "Canon EOS R5"),
        ("photographer", None, "Jane Doe"),
        ("water_quality", None, "Clear"),
        ("strobes", None, "Yes"),
        ("framing", None, "Tight"),
        ("white_balance_card", None, "Yes"),
        ("comments", None, "No issues"),
    ]

    @pytest.mark.parametrize("field_name, initial_value, new_value", fields_name_initial_new)
    def test_properties_getter_setter_and_signals(self, qtbot: QtBot, field_name: str, initial_value: object, new_value: object) -> None:
        """Model properties should have working getters, setters, and change signals."""
        # Arrange: empty MetadataModel
        model = MetadataModel()

        # Assert: fields signal correctly on change
        assert_model_property_getter_setter_and_signal(qtbot, model, field_name, initial_value, new_value)

    fields_name_invalid = [
        ("date", date(2026, 3, 24)),  # Invalid type (should be datetime)
        ("date", "not a date"),  # Invalid type
        ("latitude", 100.0),  # Must be <= 90
        ("latitude", -100.0),  # Must be >= -90
        ("longitude", 200.0),  # Must be <= 180
        ("longitude", -200.0),  # Must be >= -180
    ]

    @pytest.mark.parametrize("field_name, invalid_value", fields_name_invalid)
    def test_properties_validation(self, field_name: str, invalid_value: object) -> None:
        """Model properties should enforce type validation and constraints when set."""
        model = MetadataModel()

        with pytest.raises(ValueError):
            setattr(model, field_name, invalid_value)

    fields_name_value_normalized = [
        # Empty strings become None
        ("partner", "", None),
        ("area", "", None),
        ("site", "", None),
        ("season", "", None),
        ("transect", "", None),
        ("height", "", None),
        ("depth", "", None),
        ("camera", "", None),
        ("photographer", "", None),
        ("water_quality", "", None),
        ("strobes", "", None),
        ("framing", "", None),
        ("white_balance_card", "", None),
        ("comments", "", None),
        # Trimming whitespace
        ("partner", "  Acme Corp  ", "Acme Corp"),
        ("area", "  Coral Reef  ", "Coral Reef"),
        ("site", "  Site A  ", "Site A"),
        ("season", "  Spring  ", "Spring"),
        ("transect", "  Transect 1  ", "Transect 1"),
        ("height", " 10m ", "10m"),
        ("camera", " Canon EOS R5 ", "Canon EOS R5"),
        ("photographer", " Jane Doe ", "Jane Doe"),
        ("water_quality", " Clear ", "Clear"),
        ("strobes", " Yes ", "Yes"),
        ("framing", " Tight ", "Tight"),
        ("white_balance_card", " Yes ", "Yes"),
        ("comments", " No issues ", "No issues"),
    ]

    @pytest.mark.parametrize("field_name, input_value, expected_value", fields_name_value_normalized)
    def test_properties_normalization(self, field_name: str, input_value: object, expected_value: object) -> None:
        """Model properties should normalize (trimming, empty to None) on assignment."""
        model = MetadataModel()

        # Act: set the value
        setattr(model, field_name, input_value)

        # Assert: the value is normalized as expected
        assert getattr(model, field_name) == expected_value
