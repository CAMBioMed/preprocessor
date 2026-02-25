from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch
from pytestqt.qtbot import QtBot
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog


def test_integration_new_project_add_images_save_and_quit(
    qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """Integration test: New Project -> add images -> save -> quit.

    This test simulates the user clicking New Project in the launch dialog (we monkeypatch
    the file dialogs to avoid UI popups), then opens the main window, adds two images from
    the example set, saves the project to disk and closes the window.
    """
    # Local imports (import under test-time Qt app context)
    from preprocessor.gui.launch_dialog import LaunchDialog
    from preprocessor.gui.main_window import MainWindow
    from preprocessor.model.application_model import ApplicationModel

    # Prepare project file path in a temporary directory
    project_file = tmp_path / "test_project.pbproj"

    # Patch the save dialog used by "New Project" to return our temporary filename
    monkeypatch.setattr(
        QFileDialog,
        "getSaveFileName",
        lambda parent, title, directory, filter: (str(project_file), "Project Files (*.pbproj)"),
    )

    # Create the application model and show the launch dialog
    model = ApplicationModel()
    model.read_settings()

    launch = LaunchDialog(model)
    qtbot.addWidget(launch)
    launch.show()
    qtbot.waitExposed(launch)

    # Simulate clicking the New Project button (which will call our patched getSaveFileName)
    qtbot.mouseClick(launch.ui.btnNewProject, Qt.MouseButton.LeftButton)

    # The dialog handler should have set the current project and accepted the dialog
    assert model.current_project is not None
    # Ensure the project file was set to our temp path
    assert model.current_project.file == project_file

    # Now open the main window for that model
    main_win = MainWindow(model)
    qtbot.addWidget(main_win)
    main_win.show()
    qtbot.waitExposed(main_win)

    # Prepare example images from the repository
    repo_root = Path(__file__).resolve().parent.parent.parent
    photos_dir = (repo_root / "tests" / "preprocessor" / "photos").resolve()
    img1 = (photos_dir / "IMG_1054.JPG").resolve()
    img2 = (photos_dir / "IMG_1069.JPG").resolve()
    assert img1.exists(), f"Example image not found: {img1}"
    assert img2.exists(), f"Example image not found: {img2}"

    # Patch the open-files dialog used by the Add Photos action to return our two images
    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileNames",
        lambda parent, title, directory, filter: ([str(img1), str(img2)], "Photos (*.jpg;*.jpeg)"),
    )

    # Trigger the Add Photos action on the thumbnail dock
    main_win.thumbnail_dock.ui.addPhotoAction.trigger()

    # Wait until the photos have been added to the project (or timeout)
    qtbot.waitUntil(lambda: len(model.current_project.photos) >= 2, timeout=3000)

    assert len(model.current_project.photos) == 2

    # Trigger save action (should write the project file set earlier)
    main_win.ui.menuFile_SaveProject.trigger()

    # Ensure file was created on disk and contains the image filenames
    assert project_file.exists(), f"Project file was not written: {project_file}"
    content = project_file.read_text(encoding="utf-8")
    assert img1.name.split(".")[0] in content
    assert img2.name.split(".")[0] in content

    # Close the main window (simulate user quit)
    main_win.close()
