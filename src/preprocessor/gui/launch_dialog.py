import logging
from pathlib import Path

from PySide6.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox, QApplication

from preprocessor import app_formal_name
from preprocessor.gui.ui_launch_dialog import Ui_LaunchDialog
from preprocessor.model.project_model import ProjectModel

logger = logging.getLogger(__name__)


class LaunchDialog(QDialog):
    ui: Ui_LaunchDialog
    project_model: ProjectModel | None = None

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_LaunchDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(app_formal_name)
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.ui.btnNewProject.clicked.connect(self._handle_new_project_action)
        self.ui.btnBrowse.clicked.connect(self._handle_open_project_action)
        self.ui.btnOpenSelected.clicked.connect(self._handle_open_selected_project_action)
        self.ui.btnExit.clicked.connect(self.reject)

    def _handle_new_project_action(self) -> None:
        project_model = new_project_dialog(self, None)
        if project_model is None:
            return
        self.project_model = project_model
        self.accept()

    def _handle_open_project_action(self) -> None:
        project_model = open_project_dialog(self, None)
        if project_model is None:
            return
        self.project_model = project_model
        self.accept()

    def _handle_open_selected_project_action(self) -> None:
        # TODO: Implement
        # project = ProjectModel(ProjectData(file = Path(path)))
        # self.project_model = project
        # self.accept()
        self.reject()


def new_project(parent: QWidget | None, path: Path) -> ProjectModel | None:  # noqa: ARG001
    return ProjectModel(file=path)


def open_project(parent: QWidget | None, path: Path) -> ProjectModel | None:
    """Open the given project file and return the loaded ProjectModel, or None if failed."""
    try:
        project_model = ProjectModel.read_from_file(path)
    except FileNotFoundError as exc:
        logger.exception("Project file not found: %s", path, exc_info=exc)
        if QApplication.instance() is not None:
            QMessageBox.critical(
                parent,
                "Open Project Failed",
                f"Project file not found:\n{path}\n\n{exc}",
            )
        return None
    except ValueError as exc:
        logger.exception("Failed to open project file %s: %s", path, exc_info=exc)
        if QApplication.instance() is not None:
            QMessageBox.critical(
                parent,
                "Open Project Failed",
                f"Project file appears invalid:\n{path}\n\n{exc}",
            )
        return None
    return project_model


def save_project(parent: QWidget | None, project: ProjectModel, path: Path) -> bool:
    """Save the given project; return True if successful, False if canceled or failed."""
    try:
        project.write_to_file(path)
    except Exception as exc:
        logger.exception("Failed to save project file %s: %s", path, exc)
        if QApplication.instance() is not None:
            QMessageBox.critical(
                parent,
                "Save Project Failed",
                f"Failed to save project file:\n{path}\n\n{exc}",
            )
        return False
    return True


def new_project_dialog(parent: QWidget, old_project: ProjectModel | None) -> ProjectModel | None:
    """
    Show a file dialog to create a new project file, and return the new ProjectModel if successful,
    or None if canceled or failed.

    If `old_project` is not None and there are unsaved changes, the user will be prompted to save
    before creating a new project; if they choose to cancel, this function will return None.
    """
    # fmt: off
    path, _ = QFileDialog.getSaveFileName(
        parent,
        "New Project",
        "",
        "Project Files (*.pbproj);;All Files (*)"
    )
    # fmt: on
    if not path:
        return None
    if not save_if_dirty_dialog(parent, old_project):
        return None
    return new_project(parent, Path(path))


def open_project_dialog(parent: QWidget, old_project: ProjectModel | None) -> ProjectModel | None:
    """
    Show a file dialog to open a project file, and return the loaded ProjectModel if successful,
    or None if canceled or failed.

    If `old_project` is not None and there are unsaved changes, the user will be prompted to save
    before opening a new project; if they choose to cancel, this function will return None.
    """
    # fmt: off
    path, _ = QFileDialog.getOpenFileName(
        parent,
        "Open Project",
        "",
        "Project Files (*.pbproj);;All Files (*)"
    )
    # fmt: on
    if not path:
        return None
    if not save_if_dirty_dialog(parent, old_project):
        return None
    return open_project(parent, Path(path))


def save_project_as_dialog(parent: QWidget, project: ProjectModel) -> bool:
    """Show a file dialog to save the given project, and return True if successful, False if canceled or failed."""
    # fmt: off
    path, _ = QFileDialog.getSaveFileName(
        parent,
        "Save Project",
        str(project.file) if project.file else "",
        "Project Files (*.pbproj);;All Files (*)"
    )
    # fmt: on
    if not path:
        return False
    save_project(parent, project, Path(path))
    return True


def save_if_dirty_dialog(parent: QWidget, project: ProjectModel | None) -> bool:
    """
    If the project has unsaved changes, prompt the user to save; return True if it's now safe to proceed
    (either no unsaved changes or the user saved or chose not to save), or False if the user canceled.
    """
    if project is None or not project.dirty:
        return True
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setWindowTitle("Unsaved Changes")
    msg_box.setText("The current project has unsaved changes. Do you want to save before proceeding?")
    save_button = msg_box.addButton("Save", QMessageBox.ButtonRole.AcceptRole)
    discard_button = msg_box.addButton("Discard", QMessageBox.ButtonRole.DestructiveRole)
    msg_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
    msg_box.exec()

    clicked_button = msg_box.clickedButton()
    if clicked_button == save_button:
        return save_project(parent, project, project.file)
    return clicked_button == discard_button
