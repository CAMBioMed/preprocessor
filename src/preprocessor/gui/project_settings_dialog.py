from PySide6.QtWidgets import QDialog, QWidget

from preprocessor.gui.ui_project_settings_dialog import Ui_ProjectSettingsDialog
from preprocessor.model.project_model import ProjectModel


class ProjectSettingsDialog(QDialog):
    ui: Ui_ProjectSettingsDialog
    model: ProjectModel

    def __init__(self, model: ProjectModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.model = model
        self.ui = Ui_ProjectSettingsDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Project Settings")
        self._populate()
        self._connect_signals()

    def _populate(self) -> None:
        self.ui.txtGroup.setText(self.model.metadata_group)
        self.ui.txtArea.setText(self.model.metadata_area)
        self.ui.txtSite.setText(self.model.metadata_site)
        self.ui.txtSeason.setText(self.model.metadata_season)
        self.ui.txtDepth.setText(self.model.metadata_depth)
        self.ui.txtTransect.setText(self.model.metadata_transect)

    def _connect_signals(self) -> None:
        self.ui.btnsDialog.accepted.connect(self._handle_accept)

    def _handle_accept(self) -> None:
        self.model.metadata_group = self.ui.txtGroup.text()
        self.model.metadata_area = self.ui.txtArea.text()
        self.model.metadata_site = self.ui.txtSite.text()
        self.model.metadata_season = self.ui.txtSeason.text()
        self.model.metadata_depth = self.ui.txtDepth.text()
        self.model.metadata_transect = self.ui.txtTransect.text()
