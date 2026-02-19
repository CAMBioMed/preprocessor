import unittest

# ensure a Qt app context for QObject usage in tests if not present
from PySide6.QtCore import QCoreApplication

if QCoreApplication.instance() is None:
    QCoreApplication([])

import json
import tempfile
from pathlib import Path

from preprocessor.model.project_model import ProjectModel, ProjectData
from preprocessor.model.photo_model import PhotoModel
from preprocessor.model.qlistmodel import QListModel
import pytest


class TestProjectModel(unittest.TestCase):
    def test_photos(self) -> None:
        # Arrange
        project_model = ProjectModel(file = Path("test.pbproj"))

        # Assert initial state
        assert isinstance(project_model.photos, QListModel)
        assert project_model.photos.parent() == project_model

        # Act: add a photo
        photo0 = PhotoModel()
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
        project = ProjectModel(file = Path("test1.pbproj"))
        p = PhotoModel()
        p.original_filename = Path("picA.jpg")
        p.red_shift = (1.0, 2.0)
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
        new_project2 = ProjectModel.read_from_json(Path("test.pbproj"), json.dumps({
            "model_version": ProjectData.SERIAL_VERSION,
            "photos": [],
        }))

        # Assert: photos cleared and on_changed emitted
        assert len(new_project2.photos) == 0

    def test_save_and_load_file(self) -> None:
        # Arrange: create project with one photo
        project = ProjectModel(file = Path("test.pbproj"))
        p = PhotoModel()
        p.original_filename = Path("fileX.jpg")
        p.red_shift = (3.0, 4.0)
        project.photos.append(p)

        # Use a temporary directory and file path
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "project.json"

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
        project = ProjectModel(file = Path("test.pbproj"))

        # Initial state: clean
        assert not project.dirty

        # Act: append a photo -> project becomes dirty
        p = PhotoModel()
        project.photos.append(p)
        assert project.dirty

        # Act: mark clean externally
        project.mark_clean()
        assert not project.dirty

        # Act: change a child photo property -> project becomes dirty
        p.original_filename = "changed.jpg"
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
