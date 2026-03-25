from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QIcon


class QWorker(QObject):
    """A base class for workers that perform tasks in the background and communicate with the UI via signals."""

    on_progress: Signal = Signal(int, int)
    """Raised to report progress: processed, total"""
    on_status: Signal = Signal(str)
    """Raised to report status change: new status."""
    on_finished: Signal = Signal()
    """Raised when finished."""
    on_message: Signal = Signal(str, object)
    """Raised to report a message from the worker: message text, message icon (QIcon | str | None)"""
    on_add_item: Signal = Signal(str, str, object)
    """Raised to add an item's status to the UI: item name, item status, item icon (QIcon | str | None)"""
    on_update_item: Signal = Signal(str, str, object)
    """Raised to update an item's status in the UI: item name, new item status, new item icon (QIcon | str | None)"""

    _title: str
    """The title of the worker, used for display purposes."""
    _abort_requested: bool
    """Whether an abort has been requested."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self._title = title
        self._abort_requested = False

    @property
    def title(self) -> str:
        """Get the title to display to the user."""
        return self._title

    def request_abort(self) -> None:
        """Request the worker to abort. The worker should check `is_abort_requested()` periodically."""
        self._abort_requested = True

    def is_abort_requested(self) -> bool:
        """Check if an abort has been requested."""
        return self._abort_requested

    @Slot()
    def run(self) -> None:
        """Override this method with the worker's task."""
        pass

    @Slot()
    def handle_abort(self) -> bool:
        """Override this method to handle when an abort is requested.

        Implementations can show a dialog box asking the user whether to abort.
        When the user accepts, call `self.request_abort()` to signal the worker to stop,
        and return True to indicate the worker should be aborted.
        Otherwise, return False to continue running.

        :return: True if the worker should be aborted, False to continue.
        """
        self.request_abort()
        return True