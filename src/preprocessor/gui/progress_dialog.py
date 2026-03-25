from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QWidget, QDialogButtonBox, QStyle, QTreeWidgetItem

from preprocessor.gui.qjobs import QJobProcessor, QJob
from preprocessor.gui.ui_progress_dialog import Ui_ProgressDialog


class ProgressDialog(QDialog):
    """A dialog that shows progress on batch processing photos."""

    ui: Ui_ProgressDialog
    _processor: QJobProcessor

    def __init__(
        self,
        title: str,
        jobs: set[QJob],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(300, 100)

        self._setup_ui()
        self._connect_signals()
        # Create the processor first so initial state handlers can access its properties
        self._processor = QJobProcessor(jobs=jobs, parent=self)
        self._connect_processor()
        self._set_initial_state()
        self._add_jobs_to_ui(jobs)
        self._processor.start()

    def _setup_ui(self) -> None:
        self.ui = Ui_ProgressDialog()
        self.ui.setupUi(self)
        self.ui.treeItems.setHeaderLabels(["Item", "Status"])
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
        self._processor.on_job_end.connect(self._handle_job_end)
        self._processor.on_job_status.connect(self._handle_job_status)
        self._processor.on_job_progress.connect(self._handle_job_progress)

    def _add_jobs_to_ui(self, jobs: set[QJob]) -> None:
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
        self.ui.lstMessages.setVisible(False)  # Hide messages until we have some
        self.ui.treeItems.setVisible(False)  # Hide items until we have some

    def _handle_started(self) -> None:
        self._handle_status("Starting...")
        self.ui.lstMessages.clear()

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
        self._update_item(job, "Processing...", "info")

    def _handle_job_end(self, job: QJob, aborted: bool) -> None:
        status = "Aborted" if aborted else "Done"
        icon = "error" if aborted else "info"
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
            if item.text(0) == job.name:
                item.setText(1, status)
                actual_icon = self._determine_icon(icon)
                if actual_icon is not None:
                    item.setIcon(0, actual_icon)
                break

    def _handle_cancel(self) -> None:
        self._processor.cancel()

        # Disable the Cancel button to prevent repeated clicks
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Cancel).setEnabled(False)
        self.ui.lblStatus.setText("Cancelling...")

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
