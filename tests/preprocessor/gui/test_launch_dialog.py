from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from preprocessor.gui.model import QApplicationState
from preprocessor.gui.utils import patch_getOpenFileName_dialog


class TestLaunchDialog:
    def test_should_create_new_project_when_new_project_is_selected(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """Test that a new project can be created using the launch dialog."""
        from preprocessor.gui.launch_dialog import LaunchDialog

        # Create an empty application model
        model = QApplicationState()

        # Show the launch dialog
        launch_dialog = LaunchDialog(model)
        qtbot.addWidget(launch_dialog)
        launch_dialog.show()
        qtbot.waitExposed(launch_dialog)

        # Click the 'New Project' button
        qtbot.mouseClick(launch_dialog.ui.btnNewProject, Qt.MouseButton.LeftButton)

        # Assert: the dialog handler should have returned the project and accepted the dialog
        assert launch_dialog.project_model is not None

    def test_should_open_existing_project_when_open_project_is_selected(
        self, qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """Test that an existing project can be opened using the launch dialog."""
        from preprocessor.gui.launch_dialog import LaunchDialog

        # Create a temporary project file
        project_file = tmp_path / "test_project.pbproj"
        project_file.write_text("""{  }""")

        # Create an empty application model
        model = QApplicationState()

        # Show the launch dialog
        launch_dialog = LaunchDialog(model)
        qtbot.addWidget(launch_dialog)
        launch_dialog.show()
        qtbot.waitExposed(launch_dialog)

        # Patch the open dialog used by "Open Project" to return our temporary project file
        patch_getOpenFileName_dialog(str(project_file), monkeypatch)

        # Click the 'Browse Project' button
        qtbot.mouseClick(launch_dialog.ui.btnBrowse, Qt.MouseButton.LeftButton)

        # Assert: the dialog handler should have returned the project and accepted the dialog
        assert launch_dialog.project_model is not None
        assert launch_dialog.project_model.project_file == project_file

        # Assert: the application model's projects_path should be updated
        assert model.projects_path == project_file.parent
