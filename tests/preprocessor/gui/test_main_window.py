from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog
from pytestqt.qtbot import QtBot

from preprocessor.gui.model import QProjectModel


class TestMainWindow:
    """Tests for the MainWindow class in the preprocessor GUI."""

    def test_photos_are_added(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """Test that photos are added and the photos_path is adjusted correctly."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Create a new project
        model = QApplicationState()
        project_model = QProjectModel.new_project(None, None, None)
        assert project_model is not None
        project_dir = tmp_path / "project_dir"
        project_dir.mkdir()
        project_file = project_dir / "test_project.pbproj"
        project_model.project_file = project_file
        model.current_project = project_model

        # Copy some photos in a temporary directory beneath the project directory
        photos_dir = project_dir / "photos"
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
        reopened_project_model = QProjectModel.open_project_from_path(None, None, project_file, None)
        assert reopened_project_model is not None
        assert reopened_project_model.photos_path == photos_dir
        assert len(reopened_project_model.photos) == 2
        assert reopened_project_model.photos[0].name == photos[0].name
        assert reopened_project_model.photos[1].name == photos[1].name

    def test_directory_activation_filters_thumbnails(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """Double-clicking a directory filters thumbnails to that directory's photos."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange: create a project with a file and three photos at different depths
        model = QApplicationState()
        project_model = QProjectModel.new_project(None, None, None)
        assert project_model is not None
        project_dir = tmp_path / "project_dir"
        project_dir.mkdir()
        project_file = project_dir / "test_project.pbproj"
        project_model.project_file = project_file
        model.current_project = project_model

        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        example_photos_dir = (repo_root / "tests" / "preprocessor" / "photos").resolve()
        example_photo = (example_photos_dir / "IMG_1054.JPG").resolve()

        root_photo_path = project_dir / "ABC.jpg"
        root_photo_path.write_bytes(example_photo.read_bytes())
        nested_dir = project_dir / "x" / "y"
        nested_dir.mkdir(parents=True)
        nested_photo_path = nested_dir / "ABC.jpg"
        nested_photo_path.write_bytes(example_photo.read_bytes())
        sibling_dir = project_dir / "z"
        sibling_dir.mkdir()
        sibling_photo_path = sibling_dir / "ABC.jpg"
        sibling_photo_path.write_bytes(example_photo.read_bytes())

        photo_paths = [str(root_photo_path), str(nested_photo_path), str(sibling_photo_path)]
        monkeypatch.setattr(
            QFileDialog,
            "getOpenFileNames",
            lambda parent, title, directory, filter: (photo_paths, "Photos (*.jpg;*.jpeg)"),
        )

        main_win = MainWindow(model)
        qtbot.addWidget(main_win)
        main_win.show()
        qtbot.waitExposed(main_win)

        # Act: trigger Add Photos
        main_win.thumbnail_dock.ui.addPhotoAction.trigger()
        qtbot.waitUntil(lambda: len(model.current_project.photos) >= 3, timeout=3000)

        # Assert: initial activation is the project root, thumbnails show only the root photo
        assert main_win.tree_dock.model.active_directory == project_dir.resolve()
        thumbnail_names = [
            main_win.thumbnail_dock.ui.thumbnailListWidget.item(i).text()
            for i in range(main_win.thumbnail_dock.ui.thumbnailListWidget.count())
        ]
        assert thumbnail_names == ["ABC.jpg"]

        # Snapshot the flat project list identities and order
        flat_photos = list(model.current_project.photos)
        assert len(flat_photos) == 3

        # Act: expand root and x, then double-click y to activate it
        tree_view = main_win.tree_dock.ui.treeView
        root_index = main_win.tree_dock.model.index(0, 0)
        x_index = main_win.tree_dock.model.index(0, 0, root_index)
        y_index = main_win.tree_dock.model.index(0, 0, x_index)
        tree_view.expand(root_index)
        tree_view.expand(x_index)
        tree_view.scrollTo(y_index)

        y_rect = tree_view.visualRect(y_index)
        assert not y_rect.isNull(), "y index should be visible after expanding ancestors"
        qtbot.mouseDClick(tree_view.viewport(), Qt.MouseButton.LeftButton, pos=y_rect.center())
        # If the mouse event did not trigger activation (headless QTreeView), emit the signal directly.
        if main_win.tree_dock.model.active_directory != nested_dir.resolve():
            tree_view.doubleClicked.emit(y_index)
        qtbot.wait(100)

        # Assert: thumbnails switch to only the nested photo
        assert main_win.tree_dock.model.active_directory == nested_dir.resolve()
        thumbnail_names = [
            main_win.thumbnail_dock.ui.thumbnailListWidget.item(i).text()
            for i in range(main_win.thumbnail_dock.ui.thumbnailListWidget.count())
        ]
        assert thumbnail_names == ["ABC.jpg"]
        assert len(thumbnail_names) == 1

        # Assert: the flat project list retains the same length, identities, order, and membership
        assert list(model.current_project.photos) == flat_photos

        main_win.close()

    def test_cancel_save_on_unsaved_project_aborts_add_photos(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """Canceling the first save on an unsaved project aborts Add Photos before opening the picker."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange: create a project with no file
        model = QApplicationState()
        project_model = QProjectModel.new_project(None, None, None)
        assert project_model is not None
        model.current_project = project_model

        picker_called = False

        def _get_open_filenames(_parent: object, _title: str, _directory: str, _filter: str) -> tuple[list[str], str]:
            nonlocal picker_called
            picker_called = True
            return ([], "")

        monkeypatch.setattr(QFileDialog, "getOpenFileNames", _get_open_filenames)
        monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args, **kwargs: ("", ""))

        main_win = MainWindow(model)
        qtbot.addWidget(main_win)
        main_win.show()
        qtbot.waitExposed(main_win)

        # Act: trigger Add Photos on the unsaved project; save dialog is canceled
        main_win.thumbnail_dock.ui.addPhotoAction.trigger()

        # Assert: the photo picker was never opened
        assert not picker_called
        assert len(model.current_project.photos) == 0

        main_win.close()
