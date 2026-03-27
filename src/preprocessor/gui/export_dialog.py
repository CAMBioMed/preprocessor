from pathlib import Path

from PySide6.QtCore import QObject, QThread
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QFileDialog,
    QMessageBox,
    QDialogButtonBox,
)

from preprocessor.gui.export_photo_job import ExportPhotoJob
from preprocessor.gui.progress_dialog import ProgressDialog
from preprocessor.gui.qjobs import QJob
from preprocessor.gui.ui_export_dialog import Ui_ExportDialog
from preprocessor.model.project_model import ProjectModel


class ExportDialog(QDialog):
    current_project: ProjectModel
    ui: Ui_ExportDialog

    def __init__(self, current_project: ProjectModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.current_project = current_project
        self._worker_thread: QThread | None = None
        self._worker: QObject | None = None
        self._setup_ui()
        self._connect_signals()
        self._set_initial_state()

    def _setup_ui(self) -> None:
        self.ui = Ui_ExportDialog()
        self.ui.setupUi(self)
        self.ui.btnsDialog.button(QDialogButtonBox.StandardButton.SaveAll).setText("Export All")
        self.ui.btnsDialog.button(QDialogButtonBox.StandardButton.Cancel)

    def _connect_signals(self) -> None:
        self.ui.btnOutputDir.clicked.connect(self._handle_outputdir_browse_clicked)
        self.ui.btnsDialog.button(QDialogButtonBox.StandardButton.SaveAll).clicked.connect(self._handle_save_all)

    def _set_initial_state(self) -> None:
        # Set the output directory to the last used export path, if available
        if self.current_project.export_path:
            self.ui.txtOutputDir.setText(str(self.current_project.export_path))

    def _handle_outputdir_browse_clicked(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Output Directory")

        if directory is not None:
            self.ui.txtOutputDir.setText(str(directory))

    def _handle_save_all(self) -> None:
        # Export directory must be set and must exist
        export_dir = self.ui.txtOutputDir.text()
        if not export_dir:
            QMessageBox.warning(self, "Error", "Please specify an output directory.")
            return
        export_dir = Path(export_dir)
        try:
            export_dir.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            QMessageBox.warning(self, "Error", "The output path exists and is not a directory.")
            return

        # Save the settings
        self.current_project.export_path = export_dir

        # Show the progress UI and start export
        jobs: list[QJob] = []
        for idx, p in enumerate(self.current_project.photos):
            job = ExportPhotoJob(p, idx, export_dir)
            jobs.append(job)

        # Show progress dialog and run jobs; dialog is modal and will block until done
        dlg = ProgressDialog("Exporting Photos", jobs, parent=self, run_in_thread=True)
        dlg.exec()
