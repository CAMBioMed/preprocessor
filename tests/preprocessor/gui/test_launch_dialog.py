from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog
from _pytest.monkeypatch import MonkeyPatch
from pytestqt.qtbot import QtBot

from preprocessor.model.application_model import ApplicationModel


class TestLaunchDialog:
    def test_new_project(self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        """Test that a new project can be created using the launch dialog."""
        from preprocessor.gui.launch_dialog import LaunchDialog

        # Create an empty application model
        model = ApplicationModel()

        # Show the launch dialog
        launch_dialog = LaunchDialog(model)
        qtbot.addWidget(launch_dialog)
        launch_dialog.show()
        qtbot.waitExposed(launch_dialog)

        # Patch the save dialog used by "New Project" to return a temporary filename
        project_file = tmp_path / "test_project.pbproj"
        monkeypatch.setattr(
            QFileDialog,
            "getSaveFileName",
            lambda parent, title, directory, filter: (str(project_file), "Project Files (*.pbproj)"),
        )

        # Click the 'New Project' button
        qtbot.mouseClick(launch_dialog.ui.btnNewProject, Qt.MouseButton.LeftButton)

        # Assert: the dialog handler should have returned the project and accepted the dialog
        assert launch_dialog.project_model is not None
        assert launch_dialog.project_model.file == project_file

        # Assert: the application model's projects_path should be updated
        assert model.projects_path == project_file.parent

    def test_open_project(self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        """Test that an existing project can be opened using the launch dialog."""
        from preprocessor.gui.launch_dialog import LaunchDialog

        # Create a temporary project file
        project_file = tmp_path / "test_project.pbproj"
        project_file.write_text("""{ "model_version": 1 }""")

        # Create an empty application model
        model = ApplicationModel()

        # Show the launch dialog
        launch_dialog = LaunchDialog(model)
        qtbot.addWidget(launch_dialog)
        launch_dialog.show()
        qtbot.waitExposed(launch_dialog)

        # Patch the open dialog used by "Open Project" to return our temporary project file
        monkeypatch.setattr(
            QFileDialog,
            "getOpenFileName",
            lambda parent, title, directory, filter: (str(project_file), "Project Files (*.pbproj)"),
        )

        # Click the 'Browse Project' button
        qtbot.mouseClick(launch_dialog.ui.btnBrowse, Qt.MouseButton.LeftButton)

        # Assert: the dialog handler should have returned the project and accepted the dialog
        assert launch_dialog.project_model is not None
        assert launch_dialog.project_model.file == project_file

        # Assert: the application model's projects_path should be updated
        assert model.projects_path == project_file.parent
