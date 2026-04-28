from pathlib import Path
from typing import override

import pytest
from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from preprocessor.core.model import PhotoData
from preprocessor.gui.model import QPhotoModel
from tests.preprocessor.core.model.test_PhotoData import Test_PhotoData
from tests.preprocessor.gui.model.cls_QModelTestBase import QModelTestBase

@pytest.fixture(autouse=True)
def ensure_qapp(qapp: QApplication) -> QApplication:
    # ensure a QApplication exists for tests that rely on it
    return qapp


class Test_QPhotoModel(QModelTestBase):
    """Unit tests for QPhotoModel."""

    @override
    def create_model(self) -> QPhotoModel:
        """Helper to create a test QPhotoModel with default values."""
        return QPhotoModel(
            PhotoData(
                image_id="img_001",
                original_filename=Path("img_001.jpg").resolve(),
            )
        )

    def test_has_a_property_for_each_data_field(self) -> None:
        """Model should have a property for each field in the data model."""
        self.assert_has_a_property_for_each_data_field(QPhotoModel, PhotoData)

    @pytest.mark.parametrize(
        "field_name, initial_value, new_value",
        [(n, v, vv) for n, (v, vvs, _, _) in Test_PhotoData.fields_and_values.items() for vv in vvs],
    )
    def test_property_valid_value_and_signals(
        self,
        field_name: str,
        initial_value: object,
        new_value: object,
        qtbot: QtBot,
    ) -> None:
        self.assert_property_valid_value_and_signals(field_name, initial_value, new_value, qtbot)

    @pytest.mark.parametrize(
        "field_name, initial_value, invalid_value",
        [(n, v, iv) for n, (v, _, _, ivs) in Test_PhotoData.fields_and_values.items() for iv in ivs],
    )
    def test_property_invalid_value_and_signals(
        self,
        field_name: str,
        initial_value: object,
        invalid_value: object,
        qtbot: QtBot,
    ) -> None:
        self.assert_property_invalid_value_and_signals(field_name, initial_value, invalid_value, qtbot)

    @pytest.mark.parametrize(
        "field_name, initial_value, valid_value, input_value, expected_value",
        [(n, v, vvs[0], lv, rv) for n, (v, vvs, nvs, _) in Test_PhotoData.fields_and_values.items() for (lv, rv) in nvs],
    )
    def test_property_normalization_and_signals(
        self,
        field_name: str,
        initial_value: object,
        valid_value: object,
        input_value: object,
        expected_value: object,
        qtbot: QtBot,
    ) -> None:
        self.assert_property_normalization_and_signals(
            field_name,
            initial_value,
            valid_value,
            input_value,
            expected_value,
            qtbot,
        )