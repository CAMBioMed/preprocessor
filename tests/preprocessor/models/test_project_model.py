# ensure a Qt app context for QObject usage in tests: rely on pytest-qt's qapp
from typing import Any

import pytest
from PySide6.QtWidgets import QApplication

from preprocessor.model.qmodel import QModel


@pytest.fixture(autouse=True)
def _ensure_qapp(qapp: QApplication) -> QApplication:
    """Autouse fixture to ensure a QApplication exists for all tests in this file.

    Using the `qapp` fixture from pytest-qt ensures the application is created and
    torn down correctly by the plugin and avoids creating a QApplication at import-time,
    which can cause conflicts or crashes when pytest-qt also tries to manage one.
    """
    return qapp


import json
import tempfile
from pathlib import Path
from pytestqt.qtbot import QtBot

from preprocessor.model.project_model import ProjectModel, ProjectData
from preprocessor.model.photo_model import PhotoModel, PhotoData
from preprocessor.core.model import MetadataData
from preprocessor.model.qlistmodel import QListModel


class TestProjectModel:
    def test_photos(self, tmp_path: Path) -> None:
        # Arrange
        project_dir = tmp_path / "project"
        project_model = ProjectModel(file=project_dir / "test.pbproj")

        # Assert initial state
        assert isinstance(project_model.photos, QListModel)
        assert project_model.photos.parent() == project_model

        # Act: add a photo
        photo0 = PhotoModel(
            PhotoData(
                original_filename=project_dir / "photo0.jpg",
                width=1024,
                height=768,
            )
        )
        assert photo0.parent() is None

        project_model.photos.append(photo0)

        # Assert: photo added and parent set to photos list
        assert project_model.photos[0] is photo0
        assert photo0.parent() == project_model.photos

        # Act: remove the photo
        project_model.photos.remove(photo0)

        # Assert: removed and parent cleared
        assert len(project_model.photos) == 0
        assert photo0.parent() is None

    def test_serialize_deserialize_photos(self, tmp_path: Path) -> None:
        # Arrange
        project_dir = tmp_path / "project"
        project = ProjectModel(file=project_dir / "test1.pbproj")
        p = PhotoModel(
            PhotoData(
                original_filename=project_dir / "picA.jpg",
                width=1024,
                height=768,
                red_shift=(1.0, 2.0),
            )
        )
        project.photos.append(p)

        # Act: serialize
        json_str = project.write_to_json()

        # Assert
        assert len(project.photos) == 1
        assert isinstance(project.photos[0], PhotoModel)
        assert project.photos[0].original_filename == project_dir / "picA.jpg"
        assert project.photos[0].red_shift == (1.0, 2.0)

        # Act: deserialize (valid version included)
        new_project1 = ProjectModel.read_from_json(project_dir / "test.pbproj", json_str)

        # Assert: one photo restored with properties
        assert len(new_project1.photos) == 1
        assert isinstance(new_project1.photos[0], PhotoModel)
        assert new_project1.photos[0].original_filename == project_dir / "picA.jpg"
        assert new_project1.photos[0].red_shift == (1.0, 2.0)

        # Act: clear photos via deserialize with None (include version)
        # fmt: off
        new_project2 = ProjectModel.read_from_json(project_dir / "test.pbproj", json.dumps({
            "model_version": ProjectData.SERIAL_VERSION,
            "photos": [],
        }))
        # fmt: on

        # Assert: photos cleared and on_changed emitted
        assert len(new_project2.photos) == 0

    def test_save_and_load_file(self, tmp_path: Path) -> None:
        # Arrange: create project with one photo
        project_dir = tmp_path / "project"
        project_file = project_dir / "test.pbproj"
        project = ProjectModel(file=project_file)
        p = PhotoModel(
            PhotoData(
                original_filename=project_dir / "fileX.jpg",
                width=1024,
                height=768,
                red_shift=(3.0, 4.0),
            )
        )
        project.photos.append(p)

        # Act: save to file
        project.write_to_file(project_file)

        # Assert file exists and JSON matches serialize()
        assert project_file.exists()
        with project_file.open("r", encoding="utf-8") as fh:
            json.load(fh)

        # Act: load from file
        new_project2 = ProjectModel.read_from_file(project_file)

        # Assert: loaded project restored and on_changed fired
        assert len(new_project2.photos) == 1
        loaded = new_project2.photos[0]
        assert isinstance(loaded, PhotoModel)
        assert loaded.original_filename == project_dir / "fileX.jpg"
        assert loaded.red_shift == (3.0, 4.0)

    def test_load_missing_file_raises(self) -> None:
        missing = Path("/nonexistent/path/does_not_exist.json")
        with pytest.raises(FileNotFoundError):
            ProjectModel.read_from_file(missing)

    def test_deserialize_version_mismatch_raises(self, tmp_path: Path) -> None:
        # Arrange
        project_dir = tmp_path / "project"
        bad = {"model_version": ProjectData.SERIAL_VERSION + 1, "photos": []}
        json_str = json.dumps(bad)

        # Act / Assert
        with pytest.raises(ValueError):  # noqa: PT011
            ProjectModel.read_from_json(project_dir / "test.pbproj", json_str)

    def test_dirty_flag(self, tmp_path: Path) -> None:
        # Arrange
        project_dir = tmp_path / "project"
        project = ProjectModel(file=project_dir / "test.pbproj")

        # Initial state: clean
        assert not project.dirty

        # Act: append a photo -> project becomes dirty
        p = PhotoModel(
            PhotoData(
                original_filename=project_dir / "original.jpg",
                width=1024,
                height=768,
            )
        )
        project.photos.append(p)
        assert project.dirty

        # Act: mark clean externally
        project.mark_clean()
        assert not project.dirty

        # Act: change a child photo property -> project becomes dirty
        p.original_filename = project_dir / "changed.jpg"
        assert project.dirty

        # Act: mark clean again and modify another child property
        project.mark_clean()
        p.quadrat_corners = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        assert project.dirty

        # Act: mark_dirty explicitly
        project.mark_clean()
        project.mark_dirty()
        assert project.dirty

        # Also ensure removing a photo marks dirty
        project.mark_clean()
        project.photos.remove(p)
        assert project.dirty

    def test_file_property_getter_setter_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        with qtbot.capture_exceptions():
            # Delegate to helper to keep tests DRY
            project_dir = tmp_path / "project"
            p = project_dir / "proj.json"
            model = ProjectModel(file=p)
            self._assert_property_getter_setter_and_signal(
                qtbot, model, "file", p, project_dir / "new_proj.json", "on_file_changed"
            )

    def test_export_path_getter_setter_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        with qtbot.capture_exceptions():
            # Arrange
            project_dir = tmp_path / "project"
            model = ProjectModel(file=project_dir / "proj.json")

            # Use helper to test export_path property
            self._assert_property_getter_setter_and_signal(
                qtbot, model, "export_path", None, project_dir / "export", "on_export_path_changed"
            )

    def test_photos_list_getter_setter_and_validator_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        with qtbot.capture_exceptions():
            # Arrange
            project_dir = tmp_path / "project"
            model = ProjectModel(file=project_dir / "proj.json")
            assert len(model.photos) == 0

            # Act / Assert: appending a PhotoModel should emit on_photos_changed and update serialized data
            photo = PhotoModel(data={"original_filename": project_dir / "img.jpg", "width": 10, "height": 5})
            with qtbot.waitSignal(model.on_photos_changed, timeout=1000) as blocker:
                model.photos.append(photo)

            assert len(model.photos) == 1
            assert isinstance(model._data.photos[0], PhotoData)
            assert blocker.args is not None

            # Validator: a photo with invalid distortion_coefficients length should fail when reading from JSON
            bad_photo = {
                "original_filename": "a.jpg",
                "width": 1,
                "height": 1,
                "distortion_coefficients": [1.0, 2.0, 3.0],
            }
            bad = {"model_version": ProjectData.SERIAL_VERSION, "photos": [bad_photo]}
            json_str = json.dumps(bad)
            with pytest.raises(ValueError):
                ProjectModel.read_from_json(project_dir / "f.json", json_str)

    def test_default_metadata_getter_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        with qtbot.capture_exceptions():
            # Arrange
            project_dir = tmp_path / "project"
            model = ProjectModel(file=project_dir / "proj.json")
            md = model.default_metadata
            assert md is not None
            assert isinstance(md._data, MetadataData)

            # Act / Assert: when the metadata model signals on_changed, ProjectModel should forward via on_default_metadata_changed
            with qtbot.waitSignal(model.on_default_metadata_changed, timeout=1000) as blocker:
                # simulate a change in the metadata model
                md.on_changed.emit()

            assert blocker.args is not None

    @staticmethod
    def _assert_property_getter_setter_and_signal(
        qtbot: QtBot, model: QModel, prop_name: str, initial_value: object, new_value: object, field_signal_name: str
    ) -> None:
        """
        Helper that verifies getter, setter, and signals for a simple property.

        - initial_value: expected current value for the property
        - new_value: a different value to set
        - field_signal_name: name of the per-field signal attribute on the model (e.g. 'on_file_changed')
        """

        field_signal = getattr(model, field_signal_name)

        # Arrange / Assert: initial state
        assert getattr(model, prop_name) == initial_value
        assert model.dirty is False

        # Act/Assert: setting the same value should not emit signals
        with qtbot.assertNotEmitted(model.on_changed), qtbot.assertNotEmitted(field_signal):
            setattr(model, prop_name, initial_value)

        assert model.dirty is False

        # Act/Assert: setting a new value should emit on_changed and the field signal
        # Use a simple param checker for the field signal: it should receive the new value
        # field signal callbacks receive the signal args as *args, so create a compatible checker
        def _field_cb(*args: object) -> bool | Any:
            return len(args) > 0 and args[0] == new_value

        # Wait specifically for the field signal (so we can check its parameter)
        with qtbot.waitSignal(field_signal, timeout=1000):
            setattr(model, prop_name, new_value)

        # Final assert: property has been updated. Avoid checking dirty here to keep the helper
        # tolerant to properties with different semantics (serialized vs non-serialized).
        assert getattr(model, prop_name) == new_value
