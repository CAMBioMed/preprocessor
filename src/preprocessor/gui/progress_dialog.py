from PySide6.QtCore import QThread
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QWidget, QDialogButtonBox, QMessageBox, QListWidgetItem, QStyle, QTreeWidgetItem

from preprocessor.gui.qworker import QWorker
from preprocessor.gui.ui_progress_dialog import Ui_ProgressDialog


class ProgressDialog(QDialog):
    """A dialog that shows progress on batch processing photos."""

    ui: Ui_ProgressDialog
    _worker: QWorker | None
    _worker_thread: QThread | None

    def __init__(
        self,
        worker: QWorker,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(worker.title)
        self.setModal(True)
        self.resize(300, 100)

        self._setup_ui()
        self._connect_ui_signals()
        self._set_initial_state()

        self._connect_and_start_worker(worker)

    def _setup_ui(self) -> None:
        self.ui = Ui_ProgressDialog()
        self.ui.setupUi(self)
        self.ui.treeItems.setHeaderLabels(["Item", "Status"])
        # While a worker is running the user should be able to cancel;
        # the Close button should only be visible after finishing.
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Cancel).setVisible(True)
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Close).setVisible(False)

    def _connect_ui_signals(self) -> None:
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(self._handle_cancel)
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Close).clicked.connect(self._handle_close)

    def _connect_worker_signals(self, worker: QWorker) -> None:
        worker.on_progress.connect(self._handle_progress)
        worker.on_finished.connect(self._handle_finished)
        worker.on_status.connect(self._handle_status)
        worker.on_message.connect(self._handle_message)
        worker.on_add_item.connect(self._handle_add_item)
        worker.on_update_item.connect(self._handle_update_item)

    def _set_initial_state(self) -> None:
        self.ui.lstMessages.setVisible(False)  # Hide messages until we have some
        self.ui.treeItems.setVisible(False)  # Hide items until we have some

    def _connect_and_start_worker(self, worker: QWorker) -> None:
        # Build a background thread
        thread = QThread(self)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        self._connect_worker_signals(worker)
        thread.finished.connect(thread.deleteLater)
        # Keep references to avoid GC
        self._worker_thread = thread
        self._worker = worker
        # Let's start the work
        thread.start()

    def _handle_progress(self, processed: int, total: int) -> None:
        self.ui.prbProgress.setMaximum(total)
        self.ui.prbProgress.setValue(processed)
        self.ui.lblProgress.setText(f"{processed} / {total} ({processed / total:.1%})")

    def _handle_finished(self) -> None:
        if self._worker_thread is not None:
            self._worker_thread.quit()
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Cancel).setVisible(False)
        self.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Close).setVisible(True)
        # Clear worker references
        self._worker = None
        self._worker_thread = None

    def _handle_status(self, status: str) -> None:
        self.ui.lblStatus.setText(status)

    def _handle_message(self, text: str, icon: QIcon | str | None) -> None:
        item = QListWidgetItem(text)
        actual_icon = self._determine_icon(icon)
        if actual_icon is not None:
            item.setIcon(actual_icon)
        self.ui.lstMessages.setVisible(True)  # Ensure the messages are visible
        self.ui.lstMessages.addItem(item)

    def _handle_add_item(self, name: str, status: str, icon: QIcon | str | None) -> None:
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setText(1, status)
        actual_icon = self._determine_icon(icon)
        if actual_icon is not None:
            item.setIcon(0, actual_icon)
        self.ui.treeItems.setVisible(True)  # Ensure the items are visible
        self.ui.treeItems.addTopLevelItem(item)

    def _handle_update_item(self, name: str, status: str, icon: QIcon | str | None) -> None:
        # Find the item by name and update it
        for i in range(self.ui.treeItems.topLevelItemCount()):
            item = self.ui.treeItems.topLevelItem(i)
            if item.text(0) == name:
                item.setText(1, status)
                actual_icon = self._determine_icon(icon)
                if actual_icon is not None:
                    item.setIcon(0, actual_icon)
                break

    def _handle_cancel(self) -> None:
        if self._worker is not None:
            abort = self._worker.handle_abort()
            if not abort:
                return  # User chose not to abort, so do nothing
        self.reject()

    def _handle_close(self) -> None:
        self.accept()

    def _determine_icon(self, icon: QIcon | str | None) -> QIcon | None:
        if isinstance(icon, str):
            match icon:
                case "error": return self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
                case "warning": return self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
                case "info": return self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
                case "file": return self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
                case "dir": return self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
                case _: return None
        elif isinstance(icon, QIcon):
            return icon
        else:
            return None