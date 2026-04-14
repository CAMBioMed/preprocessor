from pathlib import Path
from typing import override, NoReturn

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytestqt.qtbot import QtBot
from PySide6.QtWidgets import QFileDialog, QApplication

from preprocessor.core.model import ProjectData, PhotoData
from preprocessor.gui.model import QProjectModel, QPhotoModel
from preprocessor.gui.model import _QProjectModel as qpm_mod
from preprocessor.gui.model import QListModel
from tests.preprocessor.core.model.test_ProjectData import Test_ProjectData
from tests.preprocessor.gui.cls_FakeMsgBox import _FakeMsgBox
from tests.preprocessor.gui.model.cls_QModelTestBase import QModelTestBase


@pytest.fixture(autouse=True)
def ensure_qapp(qapp: QApplication) -> QApplication:
    # ensure a QApplication exists for tests that rely on it
    return qapp


class Test_QProjectModel(QModelTestBase):
    """Unit tests for QProjectModel."""

    @override
    def create_model(self) -> QProjectModel:
        """Helper to create a test QProjectModel with default values."""
        return QProjectModel(
            ProjectData(),
        )

    def test_project_file_property_getter_setter_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        with qtbot.capture_exceptions():
            # Arrange
            project_dir = tmp_path / "project"
            project_file = project_dir / "proj.json"
            model = QProjectModel(ProjectData(project_file=project_file))

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
            project_model = QProjectModel()

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
        "field_name, initial_value, valid_value, input_value, expected_value",
        [(n, v, vvs[0], lv, rv) for n, (v, vvs, nvs, _) in Test_ProjectData.fields_and_values.items() for (lv, rv) in nvs],
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

class TestQProjectModelIO:
    def test_new_project_when_no_old_project_returns_model(self) -> None:
        """new_project() should return a new QProjectModel when no old project is provided."""
        # Act
        model = QProjectModel.new_project(parent=None, old_project=None, initial_dir=None)

        # Assert
        assert model is not None
        assert isinstance(model, QProjectModel)

    def test_new_project_when_old_project_not_dirty_returns_model(self, monkeypatch: MonkeyPatch) -> None:
        """new_project() should return a new QProjectModel when old project is not dirty."""
        # Arrange
        old_project = QProjectModel(ProjectData())
        assert old_project.dirty is False

        # Act
        model = QProjectModel.new_project(parent=None, old_project=old_project, initial_dir=None)

        # Assert
        assert model is not None
        assert isinstance(model, QProjectModel)

    def test_new_project_when_old_project_dirty_and_user_discards_returns_model(self, monkeypatch: MonkeyPatch) -> None:
        """new_project() should return a new QProjectModel when old project is dirty but user chooses to discard changes."""
        # Arrange
        old_project = QProjectModel(ProjectData())
        old_project.mark_dirty()
        _FakeMsgBox.next_clicked_text = "Discard"
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)

        # Act
        model = QProjectModel.new_project(parent=None, old_project=old_project, initial_dir=None)

        # Assert
        assert model is not None
        assert isinstance(model, QProjectModel)

    def test_new_project_when_old_project_dirty_and_user_cancels_returns_none(self, monkeypatch: MonkeyPatch) -> None:
        """new_project() should return None when old project is dirty and user cancels the action."""
        # Arrange
        old_project = QProjectModel(ProjectData())
        old_project.mark_dirty()
        _FakeMsgBox.next_clicked_text = "Cancel"
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)

        # Act
        model = QProjectModel.new_project(parent=None, old_project=old_project, initial_dir=None)

        # Assert
        assert model is None

    def test_open_project_from_path_when_no_old_project_returns_model(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        """open_project() should return a QProjectModel when given a valid project file path and no old project is provided."""
        # Arrange
        project_file = tmp_path / "proj.pbproj"
        pd = ProjectData()
        pd.save_to_file(project_file)
        monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *args, **kwargs: (str(project_file), ""))

        # Act
        result = QProjectModel.open_project(parent=None, old_project=None, initial_dir=tmp_path)

        # Assert
        assert result is not None
        assert isinstance(result, QProjectModel)
        assert result.project_file == project_file

    def test_open_project_from_path_when_old_project_is_not_dirty_returns_model(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        """open_project() should return a new QProjectModel when old project is not dirty."""
        # Arrange
        old_project = QProjectModel(ProjectData())
        assert old_project.dirty is False

        project_file = tmp_path / "proj.pbproj"
        pd = ProjectData()
        pd.save_to_file(project_file)
        monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *args, **kwargs: (str(project_file), ""))

        # Act
        result = QProjectModel.open_project(parent=None, old_project=old_project, initial_dir=tmp_path)

        # Assert
        assert result is not None
        assert isinstance(result, QProjectModel)
        assert result.project_file == project_file

    def test_open_project_from_path_when_old_project_is_dirty_and_user_discards_returns_model(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        """open_project() should return a new QProjectModel when old project is dirty but user chooses to discard changes."""
        # Arrange
        old_project = QProjectModel(ProjectData())
        old_project.mark_dirty()
        _FakeMsgBox.next_clicked_text = "Discard"
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)

        project_file = tmp_path / "proj.pbproj"
        pd = ProjectData()
        pd.save_to_file(project_file)
        monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *args, **kwargs: (str(project_file), ""))

        # Act
        result = QProjectModel.open_project(parent=None, old_project=old_project, initial_dir=tmp_path)

        # Assert
        assert result is not None
        assert isinstance(result, QProjectModel)
        assert result.project_file == project_file

    def test_open_project_from_path_when_old_project_is_dirty_and_user_cancels_returns_none(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        """open_project() should return None when old project is dirty and user cancels the action."""
        # Arrange
        old_project = QProjectModel(ProjectData())
        old_project.mark_dirty()
        _FakeMsgBox.next_clicked_text = "Cancel"
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)

        project_file = tmp_path / "proj.pbproj"
        pd = ProjectData()
        pd.save_to_file(project_file)
        monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *args, **kwargs: (str(project_file), ""))

        # Act
        result = QProjectModel.open_project(parent=None, old_project=old_project, initial_dir=tmp_path)

        # Assert
        assert result is None

    def test_open_project_dialog_canceled_returns_none(self, monkeypatch: MonkeyPatch) -> None:
        """open_project() should return None if the user cancels the open file dialog."""
        # Arrange
        monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *args, **kwargs: ("", ""))

        # Act
        result = QProjectModel.open_project(parent=None, old_project=None, initial_dir=None)

        # Assert
        assert result is None

    def test_save_project_to_path_success(self, tmp_path: Path) -> None:
        """save_project_to_path() should save the project to the specified path and return True on success."""
        # Arrange
        project = QProjectModel(ProjectData())
        out_file = tmp_path / "out.pbproj"

        # Act
        ok = QProjectModel.save_project_to_path(parent=None, project_model=project, path=out_file)

        # Assert
        assert ok is True
        assert out_file.exists()

    def test_save_project_without_a_project_file_calls_save_as(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        """save_project() should call save_project_as() when the project has no associated project file."""
        # Arrange
        project = QProjectModel(ProjectData())
        save_path = tmp_path / "saved.pbproj"
        monkeypatch.setattr(QProjectModel, "save_project_as", staticmethod(lambda *args, **kwargs: True))
        called = {}

        def _fake_save_as(parent: object, project: object, initial_dir: object) -> bool:
            called['ok'] = True
            return True

        monkeypatch.setattr(QProjectModel, "save_project_as", staticmethod(_fake_save_as))

        # Act
        ok = QProjectModel.save_project(parent=None, project=project, initial_dir=tmp_path)

        # Assert
        assert ok is True
        assert called.get('ok') is True

    def test_save_project_to_path_failure_shows_error_message(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        """save_project_to_path() should show an error message and return False if saving fails."""
        project = QProjectModel(ProjectData())
        out_file = tmp_path / "out.pbproj"

        def _bad_save(self: object, path: object) -> NoReturn:
            raise RuntimeError("boom")

        # Patch the ProjectData.save_to_file method at the class level (can't set arbitrary attributes
        # on pydantic model instances).
        monkeypatch.setattr(ProjectData, "save_to_file", _bad_save, raising=True)
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)

        ok = QProjectModel.save_project_to_path(parent=None, project_model=project, path=out_file)

        assert ok is False
        assert not out_file.exists()

    def test_save_project_to_path_success_and_failure(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        project = QProjectModel(ProjectData())
        out_file = tmp_path / "out.pbproj"

        ok = QProjectModel.save_project_to_path(parent=None, project_model=project, path=out_file)
        assert ok is True
        assert out_file.exists()

        def _bad_save(self: object, path: object) -> NoReturn:
            raise RuntimeError("boom")

        # Patch the ProjectData.save_to_file method at the class level (can't set arbitrary attributes
        # on pydantic model instances).
        monkeypatch.setattr(ProjectData, "save_to_file", _bad_save, raising=True)
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)

        ok2 = QProjectModel.save_project_to_path(parent=None, project_model=project, path=tmp_path / "x.pbproj")
        assert ok2 is False

    def test_save_project_calls_save_as_when_no_project_file(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        project = QProjectModel(ProjectData())
        save_path = tmp_path / "saved.pbproj"
        monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args, **kwargs: (str(save_path), ""))

        ok = QProjectModel.save_project(parent=None, project=project, initial_dir=tmp_path)

        assert ok is True
        assert save_path.exists()

    def test_save_project_as_cancel_returns_false(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args, **kwargs: ("", ""))
        project = QProjectModel(ProjectData())

        ok = QProjectModel.save_project_as(parent=None, project=project, initial_dir=None)

        assert ok is False

    def test_save_project_if_dirty_behaviour(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        assert QProjectModel.save_project_if_dirty(parent=None, project=None, initial_dir=None) is True

        clean_project = QProjectModel(ProjectData())
        assert clean_project.dirty is False
        assert QProjectModel.save_project_if_dirty(parent=None, project=clean_project, initial_dir=None) is True

        dirty_project = QProjectModel(ProjectData())
        dirty_project.mark_dirty()
        _FakeMsgBox.next_clicked_text = "Discard"
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)
        assert QProjectModel.save_project_if_dirty(parent=None, project=dirty_project, initial_dir=None) is True

        dirty_project2 = QProjectModel(ProjectData())
        dirty_project2.mark_dirty()
        _FakeMsgBox.next_clicked_text = "Cancel"
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)
        assert QProjectModel.save_project_if_dirty(parent=None, project=dirty_project2, initial_dir=None) is False

        dirty_project3 = QProjectModel(ProjectData())
        dirty_project3.mark_dirty()
        called = {}

        def _fake_save(parent: object, project: object, initial_dir: object) -> bool:
            called['ok'] = True
            return True

        monkeypatch.setattr(QProjectModel, "save_project", staticmethod(_fake_save))
        _FakeMsgBox.next_clicked_text = "Save"
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)

        assert QProjectModel.save_project_if_dirty(parent=None, project=dirty_project3, initial_dir=None) is True
        assert called.get('ok') is True

    def test_open_project_from_path_respects_save_if_dirty(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setattr(QProjectModel, "save_project_if_dirty", staticmethod(lambda *args, **kwargs: False))

        result = QProjectModel.open_project_from_path(parent=None, old_project=None, new_project_file=tmp_path / "nope.pbproj", initial_dir=None)

        assert result is None


