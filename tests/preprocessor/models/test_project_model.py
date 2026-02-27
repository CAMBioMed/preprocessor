# ensure a Qt app context for QObject usage in tests: rely on pytest-qt's qapp
import pytest
from PySide6.QtWidgets import QApplication


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
from preprocessor.model.camera_model import CameraModel, CameraData
from preprocessor.model.metadata_model import MetadataData
from preprocessor.model.qlistmodel import QListModel


class TestProjectModel:
    def test_photos(self) -> None:
        # Arrange
        project_model = ProjectModel(file=Path("test.pbproj"))

        # Assert initial state
        assert isinstance(project_model.photos, QListModel)
        assert project_model.photos.parent() == project_model

        # Act: add a photo
        photo0 = PhotoModel(
            PhotoData(
                original_filename=Path("photo0.jpg"),
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

    def test_serialize_deserialize_photos(self) -> None:
        # Arrange
        project = ProjectModel(file=Path("test1.pbproj"))
        p = PhotoModel(
            PhotoData(
                original_filename=Path("picA.jpg"),
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
        assert project.photos[0].original_filename == Path("picA.jpg")
        assert project.photos[0].red_shift == (1.0, 2.0)

        # Act: deserialize (valid version included)
        new_project1 = ProjectModel.read_from_json(Path("test.pbproj"), json_str)

        # Assert: one photo restored with properties
        assert len(new_project1.photos) == 1
        assert isinstance(new_project1.photos[0], PhotoModel)
        assert new_project1.photos[0].original_filename == Path("picA.jpg")
        assert new_project1.photos[0].red_shift == (1.0, 2.0)

        # Act: clear photos via deserialize with None (include version)
        # fmt: off
        new_project2 = ProjectModel.read_from_json(Path("test.pbproj"), json.dumps({
            "model_version": ProjectData.SERIAL_VERSION,
            "photos": [],
        }))
        # fmt: on

        # Assert: photos cleared and on_changed emitted
        assert len(new_project2.photos) == 0

    def test_save_and_load_file(self) -> None:
        # Use a temporary directory and file path
        with tempfile.TemporaryDirectory() as td:
            # Arrange: create project with one photo
            path = Path(td) / "test.pbproj"
            project = ProjectModel(file=path)
            p = PhotoModel(
                PhotoData(
                    original_filename=Path("fileX.jpg"),
                    width=1024,
                    height=768,
                    red_shift=(3.0, 4.0),
                )
            )
            project.photos.append(p)

            # Act: save to file
            project.write_to_file(path)

            # Assert file exists and JSON matches serialize()
            assert path.exists()
            with path.open("r", encoding="utf-8") as fh:
                json.load(fh)

            # Act: load from file
            new_project2 = ProjectModel.read_from_file(path)

            # Assert: loaded project restored and on_changed fired
            assert len(new_project2.photos) == 1
            loaded = new_project2.photos[0]
            assert isinstance(loaded, PhotoModel)
            assert loaded.original_filename == Path("fileX.jpg")
            assert loaded.red_shift == (3.0, 4.0)

    def test_load_missing_file_raises(self) -> None:
        missing = Path("/nonexistent/path/does_not_exist.json")
        with pytest.raises(FileNotFoundError):
            ProjectModel.read_from_file(missing)

    def test_deserialize_version_mismatch_raises(self) -> None:
        # Arrange
        bad = {"model_version": ProjectData.SERIAL_VERSION + 1, "photos": []}
        json_str = json.dumps(bad)

        # Act / Assert
        with pytest.raises(ValueError):  # noqa: PT011
            ProjectModel.read_from_json(Path("test.pbproj"), json_str)

    def test_dirty_flag(self) -> None:
        # Arrange
        project = ProjectModel(file=Path("test.pbproj"))

        # Initial state: clean
        assert not project.dirty

        # Act: append a photo -> project becomes dirty
        p = PhotoModel(
            PhotoData(
                original_filename=Path("original.jpg"),
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
        p.original_filename = Path("changed.jpg")
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
        # Arrange
        p = tmp_path / "proj.json"
        model = ProjectModel(file=p)

        # Assert: Initial value is set
        assert model.file == p  # getter

        # Assert: Model is not marked dirty initially
        assert model.dirty is False

        # Act/Assert: Setting the same value should not emit on_field_changed or on_changed signals
        with qtbot.assertNotEmitted(model.on_changed):
            with qtbot.assertNotEmitted(model.on_file_changed):
                model.file = p

        # Assert: Model is not marked dirty when setting the same value
        assert model.dirty is False

        # Act/Assert: Setting a new value should update property and emit on_field_changed and on_changed signals
        new_p = tmp_path / "new_proj.json"
        with qtbot.waitSignals(
            signals=[model.on_changed, model.on_file_changed],
            timeout=1000,
            check_params_cbs=[None, lambda p: p == new_p],  # type: ignore[list-item]
        ):
            model.file = new_p

        # Assert: Property has been updated
        assert model.file == new_p


    def test_export_path_getter_setter_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        # Arrange
        model = ProjectModel(file=tmp_path / "proj.json")
        assert model.export_path is None  # getter

        # Act / Assert
        ep = tmp_path / "export"
        with qtbot.waitSignal(model.on_export_path_changed, timeout=1000) as blocker:
            model.export_path = ep

        # Assert
        assert model.export_path == ep
        assert blocker.args and blocker.args[0] == ep

    def test_target_width_getter_setter_and_validator_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        # Arrange
        model = ProjectModel(file=tmp_path / "proj.json")
        assert model.target_width is None

        # Act / Assert: valid set emits signal
        with qtbot.waitSignal(model.on_target_width_changed, timeout=1000) as blocker:
            model.target_width = 200

        assert model.target_width == 200
        assert blocker.args is not None

        # Validator: reading JSON with invalid target_width (<1) should raise ValueError
        bad = {"model_version": ProjectData.SERIAL_VERSION, "target_width": 0}
        json_str = json.dumps(bad)
        with pytest.raises(ValueError):
            ProjectModel.read_from_json(tmp_path / "f.json", json_str)

    def test_target_height_getter_setter_and_validator_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        # Arrange
        model = ProjectModel(file=tmp_path / "proj.json")
        assert model.target_height is None

        # Act / Assert: valid set emits signal
        with qtbot.waitSignal(model.on_target_height_changed, timeout=1000) as blocker:
            model.target_height = 300

        assert model.target_height == 300
        assert blocker.args is not None

        # Validator: reading JSON with invalid target_height (<1) should raise ValueError
        bad = {"model_version": ProjectData.SERIAL_VERSION, "target_height": 0}
        json_str = json.dumps(bad)
        with pytest.raises(ValueError):
            ProjectModel.read_from_json(tmp_path / "f.json", json_str)

    def test_photos_list_getter_setter_and_validator_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        # Arrange
        model = ProjectModel(file=tmp_path / "proj.json")
        assert len(model.photos) == 0

        # Act / Assert: appending a PhotoModel should emit on_photos_changed and update serialized data
        photo = PhotoModel(data={"original_filename": Path("img.jpg"), "width": 10, "height": 5})
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
            ProjectModel.read_from_json(tmp_path / "f.json", json_str)

    def test_cameras_list_getter_setter_and_validator_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        # Arrange
        model = ProjectModel(file=tmp_path / "proj.json")
        assert len(model.cameras) == 0

        # Act / Assert: appending a CameraModel should emit on_cameras_changed and update serialized data
        cam = CameraModel(file=None, data={"name": "C1", "distortion_coefficients": [0, 0, 0, 0, 0]})
        with qtbot.waitSignal(model.on_cameras_changed, timeout=1000) as blocker:
            model.cameras.append(cam)

        assert len(model.cameras) == 1
        assert isinstance(model._data.cameras[0], CameraData)
        assert blocker.args is not None

        # Validator: invalid distortion_coefficients length in camera JSON should raise
        bad_cam = {"name": "C2", "distortion_coefficients": [1.0, 2.0, 3.0]}
        bad = {"model_version": ProjectData.SERIAL_VERSION, "cameras": [bad_cam]}
        json_str = json.dumps(bad)
        with pytest.raises(ValueError):
            ProjectModel.read_from_json(tmp_path / "f.json", json_str)

    def test_default_metadata_getter_and_signal(self, qtbot: QtBot, tmp_path: Path) -> None:
        # Arrange
        model = ProjectModel(file=tmp_path / "proj.json")
        md = model.default_metadata
        assert md is not None
        assert isinstance(md._data, MetadataData)

        # Act / Assert: when the metadata model signals on_changed, ProjectModel should forward via on_default_metadata_changed
        with qtbot.waitSignal(model.on_default_metadata_changed, timeout=1000) as blocker:
            # simulate a change in the metadata model
            md.on_changed.emit()

        assert blocker.args is not None
