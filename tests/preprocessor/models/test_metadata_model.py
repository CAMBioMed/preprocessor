import datetime
from typing import cast

from pytestqt.qtbot import QtBot

from preprocessor.model.metadata_model import MetadataModel
from preprocessor.model.qmodel import QModel
from tests.preprocessor.models.qmodel_fixture import assert_model_property_getter_setter_and_signal


class TestMetadataModel:
    def test_properties_getter_setter_and_signals(self, qtbot: QtBot) -> None:
        # Arrange: empty MetadataModel
        model = MetadataModel()

        # date
        date_val = datetime.date(2020, 1, 2)
        assert_model_property_getter_setter_and_signal(qtbot, model, "date", None, date_val)

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
            assert_model_property_getter_setter_and_signal(qtbot, model, fname, None, "X")

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
            model.date = cast(datetime.datetime, date_val)
        assert model.date == date_val
