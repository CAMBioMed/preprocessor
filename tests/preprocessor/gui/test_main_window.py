from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox
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

    def test_directory_add_recursively_imports_jpegs_in_path_order(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """Adding a directory recursively imports only JPEG files in deterministic order."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange: create a saved project and JPEG files at several depths
        model = QApplicationState()
        project = QProjectModel.new_project(None, None, None)
        assert project is not None
        project_dir = tmp_path / "project"
        source_dir = project_dir / "photos"
        nested_dir = source_dir / "nested" / "deeper"
        nested_dir.mkdir(parents=True)
        project.project_file = project_dir / "project.pbproj"
        model.current_project = project

        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        fixture_dir = repo_root / "tests" / "preprocessor" / "photos"
        expected_paths = [
            source_dir / "z.JPG",
            source_dir / "nested" / "a.jpeg",
            nested_dir / "m.jpg",
        ]
        fixture_paths = [fixture_dir / "IMG_1054.JPG", fixture_dir / "IMG_1069.JPG"]
        for index, path in enumerate(expected_paths):
            path.write_bytes(fixture_paths[index % len(fixture_paths)].read_bytes())
        (nested_dir / "ignored.png").write_bytes(fixture_paths[0].read_bytes())
        monkeypatch.setattr(
            QFileDialog,
            "getExistingDirectory",
            lambda parent, title, directory: str(source_dir),
        )

        main_win = MainWindow(model)
        qtbot.addWidget(main_win)

        # Act: trigger recursive directory addition
        main_win.thumbnail_dock.ui.addDirectoryAction.trigger()
        qtbot.waitUntil(lambda: len(project.photos) == 3, timeout=3000)

        # Assert: only JPEGs were appended, sorted by resolved path
        assert [photo.original_filename for photo in project.photos] == sorted(
            path.resolve() for path in expected_paths
        )
        assert project.photos_path == source_dir.resolve()

    def test_file_add_rejects_all_paths_when_one_is_outside_project(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """Selecting any file outside the project rejects the complete batch."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange: create one in-project path and one outside path
        model = QApplicationState()
        project = QProjectModel.new_project(None, None, None)
        assert project is not None
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        project.project_file = project_dir / "project.pbproj"
        model.current_project = project
        inside_path = (project_dir / "inside.jpg").resolve()
        outside_path = (tmp_path / "outside.jpg").resolve()
        monkeypatch.setattr(
            QFileDialog,
            "getOpenFileNames",
            lambda parent, title, directory, filter: ([str(inside_path), str(outside_path)], filter),
        )
        warnings: list[tuple[str, str]] = []
        monkeypatch.setattr(
            QMessageBox,
            "warning",
            lambda parent, title, text: warnings.append((title, text)),
        )

        main_win = MainWindow(model)
        qtbot.addWidget(main_win)

        # Act: trigger file addition
        main_win.thumbnail_dock.ui.addPhotoAction.trigger()

        # Assert: the exact containment warning is shown and nothing changes
        assert warnings == [
            (
                "Cannot Add Photos",
                "A selected or discovered path is outside the project directory:"
                f"\n{outside_path}\n\nProject directory:\n{project_dir.resolve()}",
            )
        ]
        assert len(project.photos) == 0
        assert project.photos_path is None

    def test_directory_add_rejects_outside_directory_before_traversal(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """Selecting an outside directory rejects it before recursive traversal."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange: create a saved project and an outside directory
        model = QApplicationState()
        project = QProjectModel.new_project(None, None, None)
        assert project is not None
        project_dir = tmp_path / "project"
        outside_dir = tmp_path / "outside"
        project_dir.mkdir()
        outside_dir.mkdir()
        project.project_file = project_dir / "project.pbproj"
        model.current_project = project
        monkeypatch.setattr(
            QFileDialog,
            "getExistingDirectory",
            lambda parent, title, directory: str(outside_dir),
        )
        warnings: list[tuple[str, str]] = []
        monkeypatch.setattr(
            QMessageBox,
            "warning",
            lambda parent, title, text: warnings.append((title, text)),
        )
        monkeypatch.setattr(Path, "walk", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("walk called")))

        main_win = MainWindow(model)
        qtbot.addWidget(main_win)

        # Act: trigger directory addition
        main_win.thumbnail_dock.ui.addDirectoryAction.trigger()

        # Assert: traversal did not run and the exact warning is shown
        assert warnings == [
            (
                "Cannot Add Photos",
                "A selected or discovered path is outside the project directory:"
                f"\n{outside_dir.resolve()}\n\nProject directory:\n{project_dir.resolve()}",
            )
        ]
        assert len(project.photos) == 0
        assert project.photos_path is None

    def test_ten_files_do_not_require_confirmation(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """A batch of exactly ten photos proceeds without confirmation."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange: create a saved project with ten valid JPEG paths
        model = QApplicationState()
        project = QProjectModel.new_project(None, None, None)
        assert project is not None
        project_dir = tmp_path / "project"
        photos_dir = project_dir / "photos"
        photos_dir.mkdir(parents=True)
        project.project_file = project_dir / "project.pbproj"
        model.current_project = project
        fixture = (
            Path(__file__).resolve().parent.parent.parent.parent / "tests" / "preprocessor" / "photos" / "IMG_1054.JPG"
        )
        paths = [photos_dir / f"{index:02}.jpg" for index in range(10)]
        for path in paths:
            path.write_bytes(fixture.read_bytes())
        monkeypatch.setattr(
            QFileDialog,
            "getOpenFileNames",
            lambda parent, title, directory, filter: ([str(path) for path in paths], filter),
        )
        monkeypatch.setattr(
            QMessageBox,
            "question",
            lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("confirmation shown")),
        )

        main_win = MainWindow(model)
        qtbot.addWidget(main_win)

        # Act: add exactly ten files
        main_win.thumbnail_dock.ui.addPhotoAction.trigger()
        qtbot.waitUntil(lambda: len(project.photos) == 10, timeout=3000)

        # Assert: all files were added without asking for confirmation
        assert [photo.original_filename for photo in project.photos] == [path.resolve() for path in paths]

    def test_eleven_files_can_be_declined(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """Declining an eleven-photo batch leaves the project unchanged."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange: create eleven selected paths under two directories
        model = QApplicationState()
        project = QProjectModel.new_project(None, None, None)
        assert project is not None
        project_dir = tmp_path / "project"
        first_dir = project_dir / "first"
        second_dir = project_dir / "second"
        first_dir.mkdir(parents=True)
        second_dir.mkdir()
        project.project_file = project_dir / "project.pbproj"
        model.current_project = project
        paths = [first_dir / f"{index}.jpg" for index in range(6)]
        paths.extend(second_dir / f"{index}.jpg" for index in range(5))
        monkeypatch.setattr(
            QFileDialog,
            "getOpenFileNames",
            lambda parent, title, directory, filter: ([str(path) for path in paths], filter),
        )
        questions: list[tuple[str, str, object, object]] = []

        def _decline(
            parent: object, title: str, text: str, buttons: object, default: object
        ) -> QMessageBox.StandardButton:
            questions.append((title, text, buttons, default))
            return QMessageBox.StandardButton.No

        monkeypatch.setattr(QMessageBox, "question", _decline)

        main_win = MainWindow(model)
        qtbot.addWidget(main_win)

        # Act: decline the confirmation
        main_win.thumbnail_dock.ui.addPhotoAction.trigger()

        # Assert: exact counts are shown and no state changes
        assert questions == [
            (
                "Confirm Add Photos",
                "Add 11 photos from 2 directories?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
        ]
        assert len(project.photos) == 0
        assert project.photos_path is None

    def test_eleven_files_can_be_confirmed(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """Confirming an eleven-photo batch adds every selected photo."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange: create eleven valid files under two directories
        model = QApplicationState()
        project = QProjectModel.new_project(None, None, None)
        assert project is not None
        project_dir = tmp_path / "project"
        first_dir = project_dir / "first"
        second_dir = project_dir / "second"
        first_dir.mkdir(parents=True)
        second_dir.mkdir()
        project.project_file = project_dir / "project.pbproj"
        model.current_project = project
        fixture = (
            Path(__file__).resolve().parent.parent.parent.parent / "tests" / "preprocessor" / "photos" / "IMG_1054.JPG"
        )
        paths = [first_dir / f"{index}.jpg" for index in range(6)]
        paths.extend(second_dir / f"{index}.jpg" for index in range(5))
        for path in paths:
            path.write_bytes(fixture.read_bytes())
        monkeypatch.setattr(
            QFileDialog,
            "getOpenFileNames",
            lambda parent, title, directory, filter: ([str(path) for path in paths], filter),
        )
        prompts: list[tuple[str, str]] = []

        def _accept(
            parent: object, title: str, text: str, buttons: object, default: object
        ) -> QMessageBox.StandardButton:
            prompts.append((title, text))
            return QMessageBox.StandardButton.Yes

        monkeypatch.setattr(QMessageBox, "question", _accept)

        main_win = MainWindow(model)
        qtbot.addWidget(main_win)

        # Act: confirm the batch
        main_win.thumbnail_dock.ui.addPhotoAction.trigger()
        qtbot.waitUntil(lambda: len(project.photos) == 11, timeout=3000)

        # Assert: the exact prompt was shown and every photo was added
        assert prompts == [("Confirm Add Photos", "Add 11 photos from 2 directories?")]
        assert [photo.original_filename for photo in project.photos] == [path.resolve() for path in paths]
        assert project.photos_path == first_dir.resolve()

    def test_empty_directory_reports_no_photos_added(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """An attempted empty directory import reports that no photos were added."""
        import preprocessor.gui.main_window as main_window_module
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange: create an empty in-project directory
        model = QApplicationState()
        project = QProjectModel.new_project(None, None, None)
        assert project is not None
        project_dir = tmp_path / "project"
        empty_dir = project_dir / "empty"
        empty_dir.mkdir(parents=True)
        project.project_file = project_dir / "project.pbproj"
        model.current_project = project
        monkeypatch.setattr(
            QFileDialog,
            "getExistingDirectory",
            lambda parent, title, directory: str(empty_dir),
        )
        messages: list[tuple[str, str]] = []
        monkeypatch.setattr(
            QMessageBox,
            "information",
            lambda parent, title, text: messages.append((title, text)),
        )
        monkeypatch.setattr(
            main_window_module,
            "ProgressDialog",
            lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("progress opened")),
        )

        main_win = MainWindow(model)
        qtbot.addWidget(main_win)

        # Act: attempt the empty directory import
        main_win.thumbnail_dock.ui.addDirectoryAction.trigger()

        # Assert: no progress jobs run and the exact information is shown
        assert messages == [("No Photos Added", "No photos were added.")]
        assert len(project.photos) == 0
        assert project.photos_path is None

    def test_failed_photo_job_reports_no_photos_added(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """A batch in which every photo job fails reports that no photos were added."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange: create an invalid JPEG file within a saved project
        model = QApplicationState()
        project = QProjectModel.new_project(None, None, None)
        assert project is not None
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        invalid_path = project_dir / "invalid.jpg"
        invalid_path.write_bytes(b"not an image")
        project.project_file = project_dir / "project.pbproj"
        model.current_project = project
        monkeypatch.setattr(
            QFileDialog,
            "getOpenFileNames",
            lambda parent, title, directory, filter: ([str(invalid_path)], filter),
        )
        messages: list[tuple[str, str]] = []
        monkeypatch.setattr(
            QMessageBox,
            "information",
            lambda parent, title, text: messages.append((title, text)),
        )

        main_win = MainWindow(model)
        qtbot.addWidget(main_win)

        # Act: attempt to add the invalid image
        main_win.thumbnail_dock.ui.addPhotoAction.trigger()

        # Assert: the failed batch reports zero additions and preserves state
        assert messages == [("No Photos Added", "No photos were added.")]
        assert len(project.photos) == 0
        assert project.photos_path is None

    def test_cancel_save_on_unsaved_project_aborts_add_photos(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch, auto_close_progress_dialog: object
    ) -> None:
        """Canceling the first save aborts both add flows before either picker opens."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange: create a project with no file
        model = QApplicationState()
        project_model = QProjectModel.new_project(None, None, None)
        assert project_model is not None
        model.current_project = project_model

        picker_calls = {"files": False, "directory": False}

        def _get_open_filenames(_parent: object, _title: str, _directory: str, _filter: str) -> tuple[list[str], str]:
            picker_calls["files"] = True
            return ([], "")

        def _get_existing_directory(_parent: object, _title: str, _directory: str) -> str:
            picker_calls["directory"] = True
            return ""

        monkeypatch.setattr(QFileDialog, "getOpenFileNames", _get_open_filenames)
        monkeypatch.setattr(QFileDialog, "getExistingDirectory", _get_existing_directory)
        monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args, **kwargs: ("", ""))

        main_win = MainWindow(model)
        qtbot.addWidget(main_win)
        main_win.show()
        qtbot.waitExposed(main_win)

        # Act: trigger both add actions; each canceled save must stop before source selection
        main_win.thumbnail_dock.ui.addPhotoAction.trigger()
        main_win.thumbnail_dock.ui.addDirectoryAction.trigger()

        # Assert: neither photo picker was opened
        assert picker_calls == {"files": False, "directory": False}
        assert len(model.current_project.photos) == 0

        main_win.close()
