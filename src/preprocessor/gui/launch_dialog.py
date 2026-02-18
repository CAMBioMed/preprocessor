from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox

from preprocessor.gui.ui_launch_dialog import Ui_LaunchDialog
from preprocessor.model.application_model import ApplicationModel
from preprocessor.model.project_model import ProjectModel


class LaunchDialog(QDialog):
    ui: Ui_LaunchDialog
    model: ApplicationModel

    def __init__(self, model: ApplicationModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.model = model
        self.ui = Ui_LaunchDialog()
        self.ui.setupUi(self)
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.ui.btnNewProject.clicked.connect(self._handle_new_project_action)
        self.ui.btnBrowse.clicked.connect(self._handle_open_project_action)
        self.ui.btnOpenSelected.clicked.connect(self._handle_open_selected_project_action)
        self.ui.btnExit.clicked.connect(self.reject)

    def _handle_new_project_action(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "New Project",
            "",
            "Project Files (*.pbproj);;All Files (*)"
        )
        if not path:
            self.reject()
            return
        project = ProjectModel()
        project.file = Path(path)
        self.model.current_project = project
        self.accept()


    def _handle_open_project_action(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            "",
            "Project Files (*.pbproj);;All Files (*)"
        )
        if not path:
            self.reject()
            return

        project = ProjectModel()
        try:
            project.load_from_file(path)
        except ValueError as exc:
            # Likely a serialization version mismatch or corrupt file — inform the user
            QMessageBox.critical(
                self,
                "Open Project Failed",
                f"Failed to open project file:\n{path}\n\n{exc}",
            )
            self.reject()
            return

        self.model.current_project = project
        self.accept()


    def _handle_open_selected_project_action(self) -> None:
        project = ProjectModel()
        self.model.current_project = project
        self.accept()


