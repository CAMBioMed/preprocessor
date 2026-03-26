from pathlib import Path

from PySide6.QtWidgets import QFileDialog
from _pytest.monkeypatch import MonkeyPatch
from pytestqt.qtbot import QtBot

from preprocessor.gui.launch_dialog import new_project, open_project


class TestMainWindow:
    """Tests for the MainWindow class in the preprocessor GUI."""

    def test_photos_are_added(self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object) -> None:
        """Test that photos are added and the photos_path is adjusted correctly."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.model.application_model import ApplicationModel

        # Copy some photos in a temporary directory
        photos_dir = tmp_path / "photos"
        photos_dir.mkdir()
        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        example_photos_dir = (repo_root / "tests" / "preprocessor" / "photos").resolve()
        example_photos = [
            (example_photos_dir / "IMG_1054.JPG").resolve(),
            (example_photos_dir / "IMG_1069.JPG").resolve(),
        ]
        for example_photo in example_photos:
            (photos_dir / example_photo.name).write_bytes(example_photo.read_bytes())
        photos = [photos_dir / example_photo.name for example_photo in example_photos]

        # Create a new project
        model = ApplicationModel()
        project_dir = tmp_path / "project_dir"
        project_dir.mkdir()
        project_file = project_dir / "test_project.pbproj"
        project_model = new_project(None, project_file)
        assert project_model is not None
        model.current_project = project_model

        # Open the main window
        main_win = MainWindow(model)
        qtbot.addWidget(main_win)
        main_win.show()
        qtbot.waitExposed(main_win)

        # Patch the open-files dialog used by the Add Photos action to return our two images
        monkeypatch.setattr(
            QFileDialog,
            "getOpenFileNames",
            lambda parent, title, directory, filter: ([str(p) for p in photos], "Photos (*.jpg;*.jpeg)"),
        )

        # Trigger the Add Photos action on the thumbnail dock
        main_win.thumbnail_dock.ui.addPhotoAction.trigger()
        qtbot.waitUntil(lambda: len(model.current_project.photos) >= 2, timeout=3000)
        assert len(model.current_project.photos) == 2

        # Assert: the photos are in the project and the photos_path has been adjusted
        assert model.current_project.photos_path == photos_dir
        assert model.current_project.photos[0].name == photos[0].name
        assert model.current_project.photos[1].name == photos[1].name

        # Trigger the Save action
        main_win.ui.menuFile_SaveProject.trigger()

        # Assert: the project file was created on disk and contains the image filenames
        assert project_file.exists(), f"Project file was not written: {project_file}"
        content = project_file.read_text(encoding="utf-8")
        assert photos[0].name in content
        assert photos[1].name in content

        # Close the main window (simulate user quit)
        main_win.close()

        # Open the project file again and assert the photos are still there
        reopened_project_model = open_project(None, project_file)
        assert reopened_project_model is not None
        assert reopened_project_model.photos_path == photos_dir
        assert len(reopened_project_model.photos) == 2
        assert reopened_project_model.photos[0].name == photos[0].name
        assert reopened_project_model.photos[1].name == photos[1].name
