import logging
from pathlib import Path

import cv2
import pytest
from _pytest.monkeypatch import MonkeyPatch
from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from pytestqt.qtbot import QtBot

import preprocessor.gui.main_window as main_window
import preprocessor.gui.model._q_project_model as qpm_mod
from preprocessor.core.model import PhotoData
from preprocessor.core.serialization import Point2D
from preprocessor.core.type_corners import Corners
from preprocessor.gui.main_window import MainWindow
from preprocessor.gui.model import QApplicationState, QPhotoModel, QProjectModel
from tests.preprocessor.gui.cls_FakeMsgBox import _FakeMsgBox


@pytest.fixture(autouse=True)
def discard_unsaved_changes_on_main_window_close(monkeypatch: MonkeyPatch) -> None:
    """Make unsaved-project prompts nonblocking in MainWindow tests."""
    _FakeMsgBox.next_clicked_text = "Discard"
    monkeypatch.setattr(qpm_mod, "QMessageBox", _FakeMsgBox)


@pytest.fixture
def autodetection_window(
    qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch
) -> tuple[MainWindow, QPhotoModel, QProjectModel]:
    """Show a clean project with a quadrat, rejecting any autodetection dialog."""
    source = tmp_path / "photo.jpg"
    Image.new("RGB", (64, 64)).save(source)
    model = QApplicationState()
    project = QProjectModel.new_project(None, None, None)
    assert project is not None
    project.project_file = tmp_path / "project.pbproj"
    photo = QPhotoModel(PhotoData(image_id="photo", original_filename=source))
    project.photos.append(photo)
    model.current_project = project
    corners: list[Point2D] = [(5, 5), (55, 5), (55, 55), (5, 55)]
    photo.quadrat_corners = corners
    model.current_photo = photo
    main_win = MainWindow(model)
    qtbot.addWidget(main_win)
    main_win.show()
    qtbot.waitExposed(main_win)
    photo.mark_clean()
    project.mark_clean()

    def reject_dialog(*args: object, **kwargs: object) -> None:
        pytest.fail("Autodetection must log failures without a dialog")

    for method in ("warning", "critical", "information"):
        monkeypatch.setattr(main_window.QMessageBox, method, reject_dialog)
    return main_win, photo, project


class TestMainWindow:
    """Tests for the MainWindow class in the preprocessor GUI."""

    def test_should_add_photos_when_paths_are_selected(
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

    def test_should_filter_thumbnails_when_directory_is_activated(
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

    def test_should_import_jpegs_in_path_order_when_directory_is_added(
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

    def test_should_reject_all_paths_when_one_path_is_outside_project(
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
                (
                    "A selected or discovered path is outside the project directory:"
                    f"\n{outside_path}\n\nProject directory:\n{project_dir.resolve()}"
                ),
            )
        ]
        assert len(project.photos) == 0
        assert project.photos_path is None

    def test_should_reject_directory_when_it_is_outside_project(
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
                (
                    "A selected or discovered path is outside the project directory:"
                    f"\n{outside_dir.resolve()}\n\nProject directory:\n{project_dir.resolve()}"
                ),
            )
        ]
        assert len(project.photos) == 0
        assert project.photos_path is None

    def test_should_skip_confirmation_when_exactly_ten_files_are_selected(
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

    def test_should_leave_project_unchanged_when_eleven_files_are_declined(
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

    def test_should_add_all_selected_photos_when_eleven_files_are_confirmed(
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

    def test_should_report_no_photos_added_when_directory_is_empty(
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

    def test_should_report_no_photos_added_when_all_photo_jobs_fail(
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

    def test_should_abort_add_photos_when_save_is_canceled(
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

    def test_should_keep_window_open_when_unsaved_project_close_is_canceled(
        self, qtbot: QtBot, monkeypatch: MonkeyPatch
    ) -> None:
        """Canceling the unsaved-project prompt keeps the main window open."""
        from preprocessor.gui.main_window import MainWindow
        from preprocessor.gui.model import QApplicationState

        # Arrange
        model = QApplicationState()
        project = QProjectModel.new_project(None, None, None)
        assert project is not None
        project.mark_dirty()
        model.current_project = project
        save_prompt_calls: list[tuple[object, QProjectModel | None, Path | None]] = []

        def _cancel_save_prompt(
            parent: object, current_project: QProjectModel | None, initial_dir: Path | None
        ) -> bool:
            save_prompt_calls.append((parent, current_project, initial_dir))
            return False

        monkeypatch.setattr(QProjectModel, "save_project_if_dirty", staticmethod(_cancel_save_prompt))
        main_win = MainWindow(model)
        qtbot.addWidget(main_win)
        main_win.show()
        qtbot.waitExposed(main_win)

        # Act
        main_win.close()

        # Assert
        assert main_win.isVisible()
        assert save_prompt_calls == [(main_win, project, model.projects_path)]


@pytest.mark.parametrize("error_type", [ValueError, cv2.error, RuntimeError])
def test_should_preserve_quadrat_when_autodetection_raises(
    autodetection_window: tuple[MainWindow, QPhotoModel, QProjectModel],
    monkeypatch: MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    error_type: type[Exception],
) -> None:
    """Should preserve quadrat when autodetection raises."""
    # Arrange
    main_win, photo, project = autodetection_window
    before = (photo.crop.model_dump(), photo.dirty, project.dirty)

    def fail_detection(self: main_window.DetectQuadratAnalysisJob) -> Corners:
        raise error_type("detector failure")

    monkeypatch.setattr(main_window.DetectQuadratAnalysisJob, "__call__", fail_detection)

    # Act
    with caplog.at_level(logging.ERROR, logger=main_window.__name__):
        main_win._handle_detect_quadrat_action()

    # Assert
    assert (photo.crop.model_dump(), photo.dirty, project.dirty) == before
    assert main_win.isVisible()
    record = next(record for record in caplog.records if record.name == main_window.__name__)
    assert record.levelno == logging.ERROR
    assert "autodetection failed" in record.getMessage()
    assert str(photo.original_filename) in record.getMessage()
    assert record.exc_info is not None
    assert str(record.exc_info[1]) == "detector failure"


def test_should_preserve_quadrat_when_autodetection_image_loading_fails(
    autodetection_window: tuple[MainWindow, QPhotoModel, QProjectModel],
    monkeypatch: MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Should preserve quadrat when autodetection image loading fails."""
    # Arrange
    main_win, photo, project = autodetection_window
    before = (photo.crop.model_dump(), photo.dirty, project.dirty)

    def fail_loading(path: Path) -> main_window.ImageRGB:
        raise ValueError("image loading failure")

    monkeypatch.setattr(main_window.ImageRGB, "from_file", fail_loading)

    # Act
    with caplog.at_level(logging.ERROR, logger=main_window.__name__):
        main_win._handle_detect_quadrat_action()

    # Assert
    assert (photo.crop.model_dump(), photo.dirty, project.dirty) == before
    assert main_win.isVisible()
    record = next(record for record in caplog.records if record.name == main_window.__name__)
    assert record.levelno == logging.ERROR
    assert "autodetection failed" in record.getMessage()
    assert str(photo.original_filename) in record.getMessage()
    assert record.exc_info is not None
    assert str(record.exc_info[1]) == "image loading failure"


@pytest.mark.parametrize("annotated", [True, False])
@pytest.mark.parametrize(
    "result",
    [
        Corners(()),
        Corners(((5, 5), (55, 5), (55, 55))),
        Corners(((5, 5), (15, 15), (25, 25), (35, 35))),
    ],
)
def test_should_preserve_quadrat_when_autodetection_result_is_invalid(
    autodetection_window: tuple[MainWindow, QPhotoModel, QProjectModel],
    monkeypatch: MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    result: Corners,
    annotated: bool,
) -> None:
    """Should preserve quadrat when autodetection result is invalid."""
    # Arrange
    main_win, photo, project = autodetection_window
    if not annotated:
        photo.quadrat_corners = None
        photo.mark_clean()
        project.mark_clean()
    before = (photo.crop.model_dump(), photo.dirty, project.dirty)
    monkeypatch.setattr(main_window.DetectQuadratAnalysisJob, "__call__", lambda self: result)

    # Act
    with caplog.at_level(logging.WARNING, logger=main_window.__name__):
        main_win._handle_detect_quadrat_action()

    # Assert
    assert (photo.crop.model_dump(), photo.dirty, project.dirty) == before
    assert main_win.isVisible()
    record = next(record for record in caplog.records if record.name == main_window.__name__)
    assert record.levelno == logging.WARNING
    assert "no valid quadrat" in record.getMessage()
    assert str(photo.original_filename) in record.getMessage()
    assert record.exc_info is None


def test_should_apply_quadrat_when_autodetection_succeeds_after_failure(
    autodetection_window: tuple[MainWindow, QPhotoModel, QProjectModel],
    monkeypatch: MonkeyPatch,
) -> None:
    """Should apply quadrat when autodetection succeeds after failure."""
    # Arrange
    main_win, photo, project = autodetection_window
    before = (photo.crop.model_dump(), photo.dirty, project.dirty)
    corners: list[Point2D] = [(10, 10), (50, 10), (50, 50), (10, 50)]
    calls = 0

    def detect(self: main_window.DetectQuadratAnalysisJob) -> Corners:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("first detection failed")
        return Corners(tuple(corners))

    monkeypatch.setattr(main_window.DetectQuadratAnalysisJob, "__call__", detect)

    # Act: fail through the menu entry point
    main_win.ui.menuEdit_DetectQuadrat.trigger()
    QApplication.processEvents()

    # Assert: failure leaves annotations and dirty state unchanged
    assert (photo.crop.model_dump(), photo.dirty, project.dirty) == before

    # Act: retry through the editor entry point
    main_win.editor_dock.on_autodetect_quadrat_clicked.emit()
    QApplication.processEvents()

    # Assert
    assert photo.quadrat_corners == corners
    assert main_win.isVisible()
    editor = main_win.central_widget
    assert editor._widget_points() == [editor._image_to_widget_point(x, y) for x, y in corners]
