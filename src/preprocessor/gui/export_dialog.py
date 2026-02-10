from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox, QDialogButtonBox

from preprocessor.gui.main_window2 import MainWindow2
from preprocessor.gui.ui_export_dialog import Ui_ExportDialog
from preprocessor.model.project_model import ProjectModel


class ExportDialog(QDialog):

    current_project: ProjectModel
    ui: Ui_ExportDialog

    def __init__(self, parent: MainWindow2) -> None:
        super().__init__(parent)
        assert parent.model.current_project is not None
        self.current_project = parent.model.current_project
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        self.ui = Ui_ExportDialog()
        self.ui.setupUi(self)
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.SaveAll).setText("Export All")
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.Close).setVisible(False)

        # Set the output directory to the last used export path, if available
        if self.current_project.export_path:
            self.ui.txtOutputDir.setText(str(self.current_project.export_path))

    def _connect_signals(self) -> None:
        self.ui.btnOutputDir.clicked.connect(self._handle_outputdir_browse_clicked)
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.SaveAll).clicked.connect(self._handle_save_all)
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(self._handle_cancel)
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.Close).clicked.connect(self._handle_close)

    def _handle_outputdir_browse_clicked(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Output Directory")

        if directory is not None:
            self.ui.txtOutputDir.setText(str(directory))

    def _handle_save_all(self) -> None:
        # Export directory must be set and must exist
        export_dir = self.ui.txtOutputDir.text()
        if not export_dir or not Path(export_dir).is_dir():
            QMessageBox.warning(self, "Error", "Please specify an existing output directory.")
            return

        # Disable the dialog to prevent changes while exporting
        self.ui.btnOutputDir.setEnabled(False)
        self.ui.txtOutputDir.setEnabled(False)
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.SaveAll).setEnabled(False)

        # Set the export path
        self.current_project.export_path = Path(export_dir)

        # TODO: Start export process in a background thread and update progress bar and status label

        # Show the Close button instead of the cancel button
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.Cancel).setVisible(False)
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.Close).setVisible(True)

    def _handle_cancel(self) -> None:
        # TODO: if export is in progress, ask for confirmation before canceling
        # TODO: Cancel export in progress
        self.reject()

    def _handle_close(self) -> None:
        self.accept()

