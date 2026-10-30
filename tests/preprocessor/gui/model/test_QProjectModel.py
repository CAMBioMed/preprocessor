import logging
from pathlib import Path
from typing import NoReturn, override

import pytest
from _pytest.monkeypatch import MonkeyPatch
from PySide6.QtWidgets import QApplication, QFileDialog
from pytestqt.qtbot import QtBot

import preprocessor.gui.model._q_project_model as qpm_mod
from preprocessor.core.model import PhotoData, ProjectData
from preprocessor.gui.model import QListModel, QPhotoModel, QProjectModel
from preprocessor.gui.utils import (
    patch_getOpenFileName_dialog,
    patch_getSaveFileName_dialog,
)
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

    def test_should_get_set_project_file_and_emit_signal_when_project_file_changes(
        self, qtbot: QtBot, tmp_path: Path
    ) -> None:
        """Should get and set the project file and emit a signal when it changes."""
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

    def test_should_return_photos_when_photos_are_requested(self, tmp_path: Path, qtbot: QtBot) -> None:
        """Should return photos when photos are requested."""
        with qtbot.capture_exceptions():
            # Arrange
            project_dir = tmp_path / "project"
            project_dir / "proj.json"
            project_model = QProjectModel()

            # Assert initial state
            assert isinstance(project_model.photos, QListModel)
            assert project_model.photos.parent() == project_model

            # Arrange: create a photo to add
            photo0 = QPhotoModel(
                PhotoData(
                    image_id="photo0",
                    original_filename=project_dir / "photo0.jpg",
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

    def test_should_expose_a_property_for_each_data_field_when_model_is_created(self) -> None:
        """Model should have a property for each field in the data model."""
        self.assert_has_a_property_for_each_data_field(QProjectModel, ProjectData)

    @pytest.mark.parametrize(
        ("field_name", "initial_value", "new_value"),
        [(n, v, vv) for n, (v, vvs, _, _) in Test_ProjectData.fields_and_values.items() for vv in vvs],
    )
    def test_should_accept_valid_value_and_emit_signals_when_property_is_set(
        self,
        field_name: str,
        initial_value: object,
        new_value: object,
        qtbot: QtBot,
    ) -> None:
        """Should accept a valid value and emit signals when the property is set."""
        self.assert_property_valid_value_and_signals(field_name, initial_value, new_value, qtbot)

    @pytest.mark.parametrize(
        ("field_name", "initial_value", "invalid_value"),
        [(n, v, iv) for n, (v, _, _, ivs) in Test_ProjectData.fields_and_values.items() for iv in ivs],
    )
    def test_should_reject_invalid_value_and_emit_signals_when_property_is_set(
        self,
        field_name: str,
        initial_value: object,
        invalid_value: object,
        qtbot: QtBot,
    ) -> None:
        """Should reject an invalid value and emit signals when the property is set."""
        self.assert_property_invalid_value_and_signals(field_name, initial_value, invalid_value, qtbot)

    @pytest.mark.parametrize(
        ("field_name", "initial_value", "valid_value", "input_value", "expected_value"),
        [
            (n, v, vvs[0], lv, rv)
            for n, (v, vvs, nvs, _) in Test_ProjectData.fields_and_values.items()
            for (lv, rv) in nvs
        ],
    )
    def test_should_normalize_value_and_emit_signals_when_property_is_set(
        self,
        field_name: str,
        initial_value: object,
        valid_value: object,
        input_value: object,
        expected_value: object,
        qtbot: QtBot,
    ) -> None:
        """Should normalize a value and emit signals when the property is set."""
        self.assert_property_normalization_and_signals(
            field_name,
            initial_value,
            valid_value,
            input_value,
            expected_value,
            qtbot,
        )


class TestQProjectModelIO:
    def test_should_return_model_when_new_project_has_no_old_project(self) -> None:
        """new_project() should return a new QProjectModel when no old project is provided."""
        # Act
        model = QProjectModel.new_project(parent=None, old_project=None, initial_dir=None)

        # Assert
        assert model is not None
        assert isinstance(model, QProjectModel)

    def test_should_return_model_when_old_project_is_not_dirty_during_new_project(
        self, monkeypatch: MonkeyPatch
    ) -> None:
        """new_project() should return a new QProjectModel when old project is not dirty."""
        # Arrange
        old_project = QProjectModel(ProjectData())
        assert old_project.dirty is False

        # Act
        model = QProjectModel.new_project(parent=None, old_project=old_project, initial_dir=None)

        # Assert
        assert model is not None
        assert isinstance(model, QProjectModel)

    def test_should_return_model_when_dirty_old_project_is_discarded_during_new_project(
        self, monkeypatch: MonkeyPatch
    ) -> None:
        """new_project() should return a new QProjectModel when old project is dirty but user
        chooses to discard changes."""
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

    def test_should_return_none_when_dirty_old_project_is_canceled_during_new_project(
        self, monkeypatch: MonkeyPatch
    ) -> None:
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

    def test_should_return_model_when_open_project_has_no_old_project(
        self, tmp_path: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """open_project() should return a QProjectModel when given a valid project file path and
        no old project is provided."""
        # Arrange
        project_file = tmp_path / "proj.pbproj"
        pd = ProjectData()
        pd.save_to_file(project_file)
        patch_getOpenFileName_dialog(str(project_file), monkeypatch)

        # Act
        result = QProjectModel.open_project(parent=None, old_project=None, initial_dir=tmp_path)

        # Assert
        assert result is not None
        assert isinstance(result, QProjectModel)
        assert result.project_file == project_file

    def test_should_return_model_when_old_project_is_not_dirty_during_open_project(
        self, tmp_path: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """open_project() should return a new QProjectModel when old project is not dirty."""
        # Arrange
        old_project = QProjectModel(ProjectData())
        assert old_project.dirty is False

        project_file = tmp_path / "proj.pbproj"
        pd = ProjectData()
        pd.save_to_file(project_file)
        patch_getOpenFileName_dialog(str(project_file), monkeypatch)

        # Act
        result = QProjectModel.open_project(parent=None, old_project=old_project, initial_dir=tmp_path)

        # Assert
        assert result is not None
        assert isinstance(result, QProjectModel)
        assert result.project_file == project_file

    def test_should_return_model_when_dirty_old_project_is_discarded_during_open_project(
        self, tmp_path: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """open_project() should return a new QProjectModel when old project is dirty but user
        chooses to discard changes."""
        # Arrange
        old_project = QProjectModel(ProjectData())
        old_project.mark_dirty()
        _FakeMsgBox.next_clicked_text = "Discard"
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)

        project_file = tmp_path / "proj.pbproj"
        pd = ProjectData()
        pd.save_to_file(project_file)
        patch_getOpenFileName_dialog(str(project_file), monkeypatch)

        # Act
        result = QProjectModel.open_project(parent=None, old_project=old_project, initial_dir=tmp_path)

        # Assert
        assert result is not None
        assert isinstance(result, QProjectModel)
        assert result.project_file == project_file

    def test_should_return_none_when_dirty_old_project_is_canceled_during_open_project(
        self, tmp_path: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """open_project() should return None when old project is dirty and user cancels the action."""
        # Arrange
        old_project = QProjectModel(ProjectData())
        old_project.mark_dirty()
        _FakeMsgBox.next_clicked_text = "Cancel"
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)

        project_file = tmp_path / "proj.pbproj"
        pd = ProjectData()
        pd.save_to_file(project_file)
        patch_getOpenFileName_dialog(str(project_file), monkeypatch)

        # Act
        result = QProjectModel.open_project(parent=None, old_project=old_project, initial_dir=tmp_path)

        # Assert
        assert result is None

    def test_should_return_none_when_open_project_dialog_is_canceled(self, monkeypatch: MonkeyPatch) -> None:
        """open_project() should return None if the user cancels the open file dialog."""
        # Arrange
        patch_getOpenFileName_dialog("", monkeypatch)

        # Act
        result = QProjectModel.open_project(parent=None, old_project=None, initial_dir=None)

        # Assert
        assert result is None

    def test_should_save_project_to_path_when_save_succeeds(self, tmp_path: Path) -> None:
        """save_project_to_path() should save the project to the specified path and return True on success."""
        # Arrange
        project = QProjectModel(ProjectData())
        out_file = tmp_path / "out.pbproj"

        # Act
        ok = QProjectModel.save_project_to_path(parent=None, project_model=project, path=out_file)

        # Assert
        assert ok is True
        assert out_file.exists()

    def test_should_call_save_as_when_project_has_no_project_file(
        self, tmp_path: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """save_project() should call save_project_as() when the project has no associated project file."""
        # Arrange
        project = QProjectModel(ProjectData())
        tmp_path / "saved.pbproj"
        monkeypatch.setattr(QProjectModel, "save_project_as", staticmethod(lambda *args, **kwargs: True))
        called = {}

        def _fake_save_as(parent: object, project: object, initial_dir: object) -> bool:
            called["ok"] = True
            return True

        monkeypatch.setattr(QProjectModel, "save_project_as", staticmethod(_fake_save_as))

        # Act
        ok = QProjectModel.save_project(parent=None, project=project, initial_dir=tmp_path)

        # Assert
        assert ok is True
        assert called.get("ok") is True

    def test_should_show_error_message_when_saving_project_to_path_fails(
        self,
        tmp_path: Path,
        monkeypatch: MonkeyPatch,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """save_project_to_path() should show an error message and return False if saving fails."""
        caplog.set_level(logging.CRITICAL, logger=qpm_mod.logger.name)
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

    def test_should_report_success_and_failure_when_saving_project_to_path(
        self,
        tmp_path: Path,
        monkeypatch: MonkeyPatch,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Should report success and failure when saving the project to a path."""
        project = QProjectModel(ProjectData())
        caplog.set_level(logging.CRITICAL, logger=qpm_mod.logger.name)
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

    def test_should_call_save_as_when_save_project_has_no_project_file(
        self, tmp_path: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """Should call Save As when the project has no project file."""
        project = QProjectModel(ProjectData())
        save_path = tmp_path / "saved.pbproj"
        patch_getSaveFileName_dialog(str(save_path), monkeypatch)

        ok = QProjectModel.save_project(parent=None, project=project, initial_dir=tmp_path)

        assert ok is True
        assert save_path.exists()

    def test_should_return_false_when_save_project_as_is_canceled(self, monkeypatch: MonkeyPatch) -> None:
        """Should return false when saving a project is canceled."""
        monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args, **kwargs: ("", ""))
        project = QProjectModel(ProjectData())

        ok = QProjectModel.save_project_as(parent=None, project=project, initial_dir=None)

        assert ok is False

    def test_should_return_save_if_dirty_result_when_project_dirty_state_is_checked(
        self, tmp_path: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """Should return the save-if-dirty result when the project dirty state is checked."""
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
            called["ok"] = True
            return True

        monkeypatch.setattr(QProjectModel, "save_project", staticmethod(_fake_save))
        _FakeMsgBox.next_clicked_text = "Save"
        monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)

        assert QProjectModel.save_project_if_dirty(parent=None, project=dirty_project3, initial_dir=None) is True
        assert called.get("ok") is True

    def test_should_return_none_when_open_project_respects_save_if_dirty(
        self, tmp_path: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """Should return None when opening a project respects save-if-dirty."""
        monkeypatch.setattr(QProjectModel, "save_project_if_dirty", staticmethod(lambda *args, **kwargs: False))

        result = QProjectModel.open_project_from_path(
            parent=None, old_project=None, new_project_file=tmp_path / "nope.pbproj", initial_dir=None
        )

        assert result is None
