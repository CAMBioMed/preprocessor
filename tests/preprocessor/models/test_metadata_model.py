import datetime
from pathlib import Path

import pytest
from pytestqt.qtbot import QtBot

from preprocessor.model.metadata_model import MetadataModel, MetadataData


class TestMetadataModel:
    @staticmethod
    def _assert_property_getter_setter_and_signal(
        qtbot: QtBot, model: MetadataModel, prop_name: str, initial_value, new_value, field_signal_name: str
    ) -> None:
        """Helper to assert getter, setter, and per-field signal emission for MetadataModel properties."""
        getter = lambda: getattr(model, prop_name)
        field_signal = getattr(model, field_signal_name)

        # initial
        assert getter() == initial_value

        # Setting the same value: MetadataModel setters emit the per-field signal unconditionally
        with qtbot.waitSignal(field_signal, timeout=1000):
            setattr(model, prop_name, initial_value)

        # setting a different value emits the field signal
        with qtbot.waitSignal(field_signal, timeout=1000):
            setattr(model, prop_name, new_value)

        # getter updated
        assert getter() == new_value

    def test_properties_getter_setter_and_signals(self, qtbot: QtBot) -> None:
        # Arrange: empty MetadataModel
        model = MetadataModel()

        # date
        date_val = datetime.date(2020, 1, 2)
        self._assert_property_getter_setter_and_signal(qtbot, model, "date", None, date_val, "on_date_changed")

        # string fields: partner, area, site, season, transect, height, latitude, longitude, depth, camera,
        # photographer, water_quality, strobes, framing, white_balance_card, comments
        str_fields = [
            "partner",
            "area",
            "site",
            "season",
            "transect",
            "height",
            "latitude",
            "longitude",
            "depth",
            "camera",
            "photographer",
            "water_quality",
            "strobes",
            "framing",
            "white_balance_card",
            "comments",
        ]

        for fname in str_fields:
            self._assert_property_getter_setter_and_signal(qtbot, model, fname, None, "X", f"on_{fname}_changed")

    def test_validator_trim_and_empty_to_none_on_creation(self) -> None:
        # Validator runs on model validation/creation: whitespace-only -> None, trimming applied
        data = {
            "partner": "  Acme  ",
            "comments": "   ",
        }
        model = MetadataModel(data=data)

        assert model.partner == "Acme"
        # whitespace-only comments should be normalized to None
        assert model.comments is None

    def test_date_setter_accepts_date_and_signal(self, qtbot: QtBot) -> None:
        model = MetadataModel()
        date_val = datetime.date(1999, 12, 31)
        with qtbot.waitSignal(model.on_date_changed, timeout=1000):
            model.date = date_val
        assert model.date == date_val

