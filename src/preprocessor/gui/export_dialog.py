from pathlib import Path
import time

from PySide6.QtCore import Signal, Slot, QObject, QThread
from PySide6.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox, QDialogButtonBox

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

        # Disable UI controls while exporting
        self.ui.btnOutputDir.setEnabled(False)
        self.ui.txtOutputDir.setEnabled(False)
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.SaveAll).setEnabled(False)

        # Set the export path
        self.current_project.export_path = Path(export_dir)

        # Prepare progress UI
        self.ui.prbProgress.setValue(0)
        self.ui.prbProgress.setMaximum(max(1, len(list(self.current_project.photos))))
        self.ui.lblProgress_Status.setText("Starting export...")

        # Start export worker in background thread
        worker = _ExportWorker(self.current_project)
        thread = QThread(self)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.progress.connect(self._on_worker_progress)
        worker.status.connect(self._on_worker_status)
        worker.finished.connect(self._on_worker_finished)
        worker.finished.connect(thread.quit)
        thread.finished.connect(thread.deleteLater)
        # keep refs to avoid GC
        self._worker_thread = thread
        self._worker = worker
        thread.start()

        # Show Close only after finished; keep Cancel visible for cancellation
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.Cancel).setVisible(True)
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.Close).setVisible(False)

    @Slot(int, int)
    def _on_worker_progress(self, processed: int, total: int) -> None:
        # Update progress bar using count-based progress
        self.ui.prbProgress.setMaximum(max(1, total))
        self.ui.prbProgress.setValue(processed)

    @Slot(str)
    def _on_worker_status(self, text: str) -> None:
        self.ui.lblProgress_Status.setText(text)

    @Slot()
    def _on_worker_finished(self) -> None:
        # Re-enable UI
        self.ui.btnOutputDir.setEnabled(True)
        self.ui.txtOutputDir.setEnabled(True)
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.SaveAll).setEnabled(True)
        # Swap Cancel -> Close
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.Cancel).setVisible(False)
        self.ui.dialogButtons.button(QDialogButtonBox.StandardButton.Close).setVisible(True)
        # Clear worker refs
        self._worker = None
        self._worker_thread = None
        self.ui.lblProgress_Status.setText("Export finished.")

    def _handle_cancel(self) -> None:
        # If export in progress, ask for confirmation before canceling
        if self._worker is not None:
            res = QMessageBox.question(
                self,
                "Cancel export",
                "An export is in progress. Do you want to cancel?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if res == QMessageBox.StandardButton.Yes:
                # request stop; worker checks periodically
                if hasattr(self._worker, "request_stop"):
                    self._worker.request_stop()
                    self.ui.lblProgress_Status.setText("Canceling...")
                # do not close dialog immediately; wait for worker to finish cleaning up
            return

        # No export in progress -> just reject
        self.reject()

    def _handle_close(self) -> None:
        self.accept()


class _ExportWorker(QObject):
    """
    Background worker that exports photos one by one.
    Emits progress and status updates; real export not implemented.
    """
    progress: Signal = Signal(int, int)  # processed, total
    status: Signal = Signal(str)
    finished: Signal = Signal()

    def __init__(self, project: ProjectModel) -> None:
        super().__init__()
        self.project = project
        self._stop_requested = False

    @Slot()
    def run(self) -> None:
        photos = list(self.project.photos)
        total = len(photos)
        if total == 0:
            self.status.emit("No photos to export.")
            self.progress.emit(0, 0)
            self.finished.emit()
            return

        for idx, photo in enumerate(photos, start=1):
            if self._stop_requested:
                self.status.emit("Export canceled.")
                break
            # Update status
            name = Path(photo.original_filename).name if photo.original_filename else f"photo {idx}"
            self.status.emit(f"Exporting {idx}/{total}: {name}")
            # TODO: perform actual export of `photo` to self.project.export_path
            # Simulate work (short sleep)
            time.sleep(0.05)
            # report progress
            self.progress.emit(idx, total)

        self.finished.emit()

    def request_stop(self) -> None:
        self._stop_requested = True

