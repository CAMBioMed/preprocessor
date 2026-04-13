from pathlib import Path
from typing import override

import pytest
from pytestqt.qtbot import QtBot

from preprocessor.core.model import ProjectData, PhotoData
from preprocessor.gui.model import QProjectModel, QPhotoModel
from preprocessor.model.qlistmodel import QListModel
from tests.preprocessor.core.model.test_ProjectData import Test_ProjectData
from tests.preprocessor.gui.model.cls_QModelTestBase import QModelTestBase


class Test_QProjectModel(QModelTestBase):
    """Unit tests for QProjectModel."""

    @override
    def create_model(self) -> QProjectModel:
        """Helper to create a test QProjectModel with default values."""
        return QProjectModel(
            project_file=Path("project/proj.json").resolve(),
            data=ProjectData(),
        )

    def test_project_file_property_getter_setter_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        with qtbot.capture_exceptions():
            # Arrange
            project_dir = tmp_path / "project"
            project_file = project_dir / "proj.json"
            model = QProjectModel(project_file=project_file)

            # Act
            self.assert_model_property_getter_setter_and_signal(
                model,
                "project_file",
                project_file,
                project_dir / "new_proj.json",
                qtbot,
            )

    def test_photos(self, tmp_path: Path, qtbot: QtBot) -> None:
        with qtbot.capture_exceptions():
            # Arrange
            project_dir = tmp_path / "project"
            project_file = project_dir / "proj.json"
            project_model = QProjectModel(project_file=project_file)

            # Assert initial state
            assert isinstance(project_model.photos, QListModel)
            assert project_model.photos.parent() == project_model

            # Arrange: create a photo to add
            photo0 = QPhotoModel(
                PhotoData(
                    image_id="photo0",
                    image_path=project_dir / "photo0.jpg",
                )
            )
            assert photo0.parent() is None

            # Act: add the photo
            with qtbot.waitSignal(project_model.on_photos_changed, timeout=1000):
                project_model.photos.append(photo0)

            # Assert: photo added and parent set to photos list
            assert project_model.photos[0] is photo0
            assert photo0.parent() == project_model.photos

            # Act: remove the photo
            with qtbot.waitSignal(project_model.on_photos_changed, timeout=1000):
                project_model.photos.remove(photo0)

            # Assert: photo is removed and its parent cleared
            assert len(project_model.photos) == 0
            assert photo0.parent() is None


    def test_has_a_property_for_each_data_field(self) -> None:
        """Model should have a property for each field in the data model."""
        self.assert_has_a_property_for_each_data_field(QProjectModel, ProjectData)

    @pytest.mark.parametrize(
        "field_name, initial_value, new_value",
        [(n, v, vv) for n, (v, vvs, _, _) in Test_ProjectData.fields_and_values.items() for vv in vvs],
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
        [(n, v, iv) for n, (v, _, _, ivs) in Test_ProjectData.fields_and_values.items() for iv in ivs],
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
        "field_name, initial_value, input_value, expected_value",
        [(n, v, lv, rv) for n, (v, _, nvs, _) in Test_ProjectData.fields_and_values.items() for (lv, rv) in nvs],
    )
    def test_property_normalization_and_signals(
        self,
        field_name: str,
        initial_value: object,
        input_value: object,
        expected_value: object,
        qtbot: QtBot,
    ) -> None:
        self.assert_property_normalization_and_signals(field_name, initial_value, input_value, expected_value, qtbot)
