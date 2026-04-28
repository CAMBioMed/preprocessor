import logging

from PySide6.QtWidgets import QDialog, QWidget

from preprocessor import app_formal_name
from preprocessor.gui.ui_launch_dialog import Ui_LaunchDialog
from preprocessor.gui.model._QApplicationState import QApplicationState
from preprocessor.gui.model._QProjectModel import QProjectModel

logger = logging.getLogger(__name__)


class LaunchDialog(QDialog):
    ui: Ui_LaunchDialog
    application_model: QApplicationState
    project_model: QProjectModel | None = None

    def __init__(self, model: QApplicationState, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_LaunchDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(app_formal_name)

        self.application_model = model
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.ui.btnNewProject.clicked.connect(self._handle_new_project_action)
        self.ui.btnBrowse.clicked.connect(self._handle_open_project_action)
        self.ui.btnOpenSelected.clicked.connect(self._handle_open_selected_project_action)
        self.ui.btnExit.clicked.connect(self.reject)

    def _handle_new_project_action(self) -> None:
        project_model = QProjectModel.new_project(self, None, self.application_model.projects_path)
        if project_model is None:
            return
        self.application_model.projects_path = (
            project_model.project_file.parent if project_model.project_file else self.application_model.projects_path
        )
        self.project_model = project_model
        self.accept()

    def _handle_open_project_action(self) -> None:
        project_model = QProjectModel.open_project(self, None, self.application_model.projects_path)
        if project_model is None:
            return
        self.application_model.projects_path = (
            project_model.project_file.parent if project_model.project_file else self.application_model.projects_path
        )
        self.project_model = project_model
        self.accept()

    def _handle_open_selected_project_action(self) -> None:
        # TODO: Implement
        # project = QProjectModel(ProjectData(project_file = Path(path)))
        # self.project_model = project
        # self.accept()
        self.reject()
