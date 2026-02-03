from pathlib import Path

from PySide6.QtWidgets import QDialog, QWidget, QFileDialog

from preprocessor.gui.ui_export_dialog import Ui_ExportDialog


class ExportDialog(QDialog):

    ui: Ui_ExportDialog

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_ExportDialog()
        self.ui.setupUi(self)
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.ui.btnOutputDir.clicked.connect(self._handle_outputdir_browse_clicked)
        # self.ui.dialogButtons.accepted.connect(self._handle_accepted)
        # self.ui.dialogButtons.rejected.connect(self._handle_rejected)

    def _handle_outputdir_browse_clicked(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Output Directory")

        if directory is not None:
            self.ui.txtOutputDir.setText(str(directory))

    # def _handle_accepted(self) -> None:
    #     self.accept()
    #
    # def _handle_rejected(self) -> None:
    #     self.reject()

