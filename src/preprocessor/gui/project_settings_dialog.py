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
        self.ui.txtPartner.setText(self.model.default_metadata.partner)
        self.ui.txtArea.setText(self.model.default_metadata.area)
        self.ui.txtSite.setText(self.model.default_metadata.site)
        self.ui.txtSeason.setText(self.model.default_metadata.season)
        self.ui.txtDepth.setText(self.model.default_metadata.depth)
        self.ui.txtTransect.setText(self.model.default_metadata.transect)

    def _connect_signals(self) -> None:
        self.ui.btnsDialog.accepted.connect(self._handle_accept)

    def _handle_accept(self) -> None:
        self.model.default_metadata.partner = self.ui.txtPartner.text()
        self.model.default_metadata.area = self.ui.txtArea.text()
        self.model.default_metadata.site = self.ui.txtSite.text()
        self.model.default_metadata.season = self.ui.txtSeason.text()
        self.model.default_metadata.depth = self.ui.txtDepth.text()
        self.model.default_metadata.transect = self.ui.txtTransect.text()
