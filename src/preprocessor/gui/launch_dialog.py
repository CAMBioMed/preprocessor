import logging
from pathlib import Path

from PySide6.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox

from preprocessor.gui.ui_launch_dialog import Ui_LaunchDialog
from preprocessor.model.application_model import ApplicationModel
from preprocessor.model.project_model import ProjectModel

logger = logging.getLogger(__name__)

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
        new_project = new_project_dialog(self, None)
        if new_project is None:
            self.reject()
            return
        self.model.current_project = new_project
        self.accept()


    def _handle_open_project_action(self) -> None:
        new_project = open_project_dialog(self, None)
        if new_project is None:
            self.reject()
            return
        self.model.current_project = new_project
        self.accept()


    def _handle_open_selected_project_action(self) -> None:
        # TODO: Implement
        # project = ProjectModel(ProjectData(file = Path(path)))
        # self.model.current_project = project
        # self.accept()
        self.reject()


def new_project_dialog(parent: QWidget, old_project: ProjectModel | None) -> ProjectModel | None:
    """
    Show a file dialog to create a new project file, and return the new ProjectModel if successful,
    or None if canceled or failed.

    If `old_project` is not None and there are unsaved changes, the user will be prompted to save
    before creating a new project; if they choose to cancel, this function will return None.
    """
    path, _ = QFileDialog.getSaveFileName(
        parent,
        "New Project",
        "",
        "Project Files (*.pbproj);;All Files (*)"
    )
    if not path:
        return None
    if not save_if_dirty_dialog(parent, old_project):
        return None
    new_project = ProjectModel(file=Path(path))
    return new_project


def open_project_dialog(parent: QWidget, old_project: ProjectModel | None) -> ProjectModel | None:
    """
    Show a file dialog to open a project file, and return the loaded ProjectModel if successful,
    or None if canceled or failed.

    If `old_project` is not None and there are unsaved changes, the user will be prompted to save
    before opening a new project; if they choose to cancel, this function will return None.
    """
    path, _ = QFileDialog.getOpenFileName(
        parent,
        "Open Project",
        "",
        "Project Files (*.pbproj);;All Files (*)"
    )
    if not path:
        return None
    if not save_if_dirty_dialog(parent, old_project):
        return None
    try:
        new_project = ProjectModel.read_from_file(path)
    except ValueError as exc:
        logger.exception("Failed to open project file %s: %s", path, exc)
        QMessageBox.critical(
            parent,
            "Open Project Failed",
            f"Failed to open project file:\n{path}\n\n{exc}",
        )
        return None
    return new_project

def save_project_dialog(parent: QWidget, project: ProjectModel, path: Path) -> bool:
    """
    Save the given project, prompting for a file path if it doesn't have one yet;
    return True if successful, False if canceled or failed.
    """
    try:
        project.write_to_file(path)
    except Exception as exc:
        logger.exception("Failed to save project file %s: %s", path, exc)
        QMessageBox.critical(
            parent,
            "Save Project Failed",
            f"Failed to save project file:\n{path}\n\n{exc}",
        )
        return False
    return True


def save_project_as_dialog(parent: QWidget, project: ProjectModel) -> bool:
    """Show a file dialog to save the given project, and return True if successful, False if canceled or failed."""
    path, _ = QFileDialog.getSaveFileName(
        parent,
        "Save Project",
        str(project.file) if project.file else "",
        "Project Files (*.pbproj);;All Files (*)"
    )
    if not path:
        return False
    save_project_dialog(parent, project, Path(path))
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
        return save_project_dialog(parent, project, project.file)
    return clicked_button == discard_button
