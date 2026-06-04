from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QWidget, QDialogButtonBox, QStyle, QTreeWidgetItem
from PySide6.QtCore import QTimer
import contextlib

from collections.abc import Iterable

from preprocessor.gui.jobs.qjobs import QJobProcessor, QJob
from preprocessor.gui.ui_progress_dialog import Ui_ProgressDialog


class ProgressDialog(QDialog):
    """A dialog that shows progress on batch processing photos."""

    ui: Ui_ProgressDialog
    _processor: QJobProcessor

    def __init__(
        self,
        title: str,
        jobs: Iterable[QJob],
        parent: QWidget | None = None,
        run_in_thread: bool = True,
        auto_close_on_finish: bool = False,
    ) -> None:
        super().__init__(parent)

        self._setup_ui()
        self.setWindowTitle(title)
        self.setModal(True)
        self._connect_signals()
        # Create the processor first so initial state handlers can access its properties
        self._processor = QJobProcessor(jobs=jobs, parent=self, run_in_thread=run_in_thread)
        # Optionally auto-close the dialog when processing finishes (useful for tests)
        if auto_close_on_finish:
            self._processor.on_finished.connect(lambda: QTimer.singleShot(0, self.accept))
        self._connect_processor()
        self._set_initial_state()
        self._add_jobs_to_ui(jobs)
        self._processor.start()

    def _setup_ui(self) -> None:
        self.ui = Ui_ProgressDialog()
        self.ui.setupUi(self)
        # Use standard Cancel/Close buttons so tests (and other code) can find them
        self.ui.btnDialogButtons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Close
        )
        # Keep references to the actual QPushButton objects
        self._cancel_button = self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Cancel)
        self._close_button = self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Close)
        # Disconnect any default accepted/rejected handlers if present
        with contextlib.suppress(Exception):
            self.ui.btnDialogButtons.accepted.disconnect()
            self.ui.btnDialogButtons.rejected.disconnect()
        # Show the columns
        self.ui.treeItems.setHeaderLabels(["Item", "Status"])
        self.ui.treeItems.header().setStretchLastSection(False)
        self.ui.treeItems.header().setSectionResizeMode(0, self.ui.treeItems.header().ResizeMode.Stretch)
        self.ui.treeItems.header().setSectionResizeMode(1, self.ui.treeItems.header().ResizeMode.Fixed)
        self.ui.treeItems.header().resizeSection(0, 80)
        # While a worker is running the user should be able to cancel;
        # the Close button should only be visible after finishing.
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Cancel).setVisible(True)
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Close).setVisible(False)

    def _connect_signals(self) -> None:
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(self._handle_cancel)
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Close).clicked.connect(self._handle_close)

    def _connect_processor(self) -> None:
        self._processor.on_started.connect(self._handle_started)
        self._processor.on_progress.connect(self._handle_progress)
        self._processor.on_finished.connect(self._handle_finished)
        self._processor.on_status.connect(self._handle_status)
        self._processor.on_job_start.connect(self._handle_job_start)
        self._processor.on_job_success.connect(self._handle_job_success)
        self._processor.on_job_failed.connect(self._handle_job_failed)
        self._processor.on_job_status.connect(self._handle_job_status)
        self._processor.on_job_progress.connect(self._handle_job_progress)

    def _add_jobs_to_ui(self, jobs: Iterable[QJob]) -> None:
        for job in jobs:
            item = QTreeWidgetItem()
            item.setText(0, job.name)
            item.setText(1, "")
            actual_icon = self._determine_icon("file")
            if actual_icon is not None:
                item.setIcon(0, actual_icon)
            self.ui.treeItems.addTopLevelItem(item)

    def _set_initial_state(self) -> None:
        self._handle_status("Ready.")
        self._handle_progress(0, self._processor.total)

    def _handle_started(self) -> None:
        self._handle_status("Starting...")

    def _handle_progress(self, processed: int, total: int) -> None:
        self.ui.prbProgress.setMaximum(total)
        self.ui.prbProgress.setValue(processed)
        self.ui.lblProgress.setText(f"{processed} / {total} ({processed / total:.1%})")

    def _handle_finished(self, aborted: bool) -> None:
        if aborted:
            self._handle_status("Cancelled.")
        else:
            self._handle_status("Done.")

        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Cancel).setVisible(False)
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Close).setVisible(True)

    def _handle_status(self, status: str) -> None:
        self.ui.lblStatus.setText(status)

    def _handle_job_start(self, job: QJob) -> None:
        self._update_item(job, "Processing...", "file")

    def _handle_job_success(self, job: QJob, _result: object) -> None:
        status = "Done"
        icon = "file"
        self._update_item(job, status, icon)

    def _handle_job_failed(self, job: QJob, aborted: bool) -> None:
        status = "Aborted" if aborted else "Errored"
        icon = "error"
        self._update_item(job, status, icon)

    def _handle_job_status(self, job: QJob, status: str, icon: QIcon | str | None) -> None:
        self._update_item(job, status, icon)

    def _handle_job_progress(self, job: QJob, steps: int, total_steps: int) -> None:
        progress_text = f"{steps} / {total_steps} ({steps / total_steps:.1%})"
        self._update_item(job, progress_text, None)

    def _update_item(self, job: QJob, status: str, icon: QIcon | str | None) -> None:
        # Find the item by name and update it
        for i in range(self.ui.treeItems.topLevelItemCount()):
            item = self.ui.treeItems.topLevelItem(i)
            if item is None:  # Just in case, but should not happen
                continue
            if item.text(0) == job.name:
                item.setText(1, status)
                actual_icon = self._determine_icon(icon)
                if actual_icon is not None:
                    item.setIcon(0, actual_icon)
                break

    def _handle_cancel(self) -> None:
        # Disable the Cancel button to prevent repeated clicks
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Cancel).setEnabled(False)
        self.ui.lblStatus.setText("Cancelling...")

        self._processor.cancel()

    def _handle_close(self) -> None:
        self.accept()

    def _determine_icon(self, icon: QIcon | str | None) -> QIcon | None:
        if isinstance(icon, str):
            match icon:
                case "error":
                    return self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
                case "warning":
                    return self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
                case "info":
                    return self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
                case "file":
                    return self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
                case "dir":
                    return self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
                case _:
                    return None
        elif isinstance(icon, QIcon):
            return icon
        else:
            return None
