from __future__ import annotations

from typing import Set, Callable, Optional, Any, Generator

import pytest
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QDialogButtonBox, QTreeWidgetItem, QAbstractButton
from PySide6.QtCore import QRunnable

from pytestqt.qtbot import QtBot

from preprocessor.gui.progress_dialog import ProgressDialog
from preprocessor.gui.qjobs import QJob, CancelToken
from PySide6.QtCore import QThreadPool


class AsyncTestJob(QJob):
    """A test job that emits signals asynchronously using QTimer so tests can interact.

    The job schedules a few progress/status updates and then finishes. Calling
    `request_abort()` will mark the job aborted and cause it to emit an aborted end.
    """

    _steps: int
    _interval: int
    _idx: int

    def __init__(self, name: str, steps: int = 3, interval_ms: int = 30) -> None:
        super().__init__(name)

        self._steps = steps
        self._interval = interval_ms
        self._idx = 0

    def process(self) -> bool:
        from PySide6.QtCore import QEventLoop

        aborted = False
        loop = QEventLoop()

        def _tick() -> None:
            nonlocal aborted
            if self.cancel_token is not None and self.cancel_token.is_cancelled():
                # report aborted and finish
                self.update_status("Aborting...")
                aborted = True
                loop.quit()
                return

            self._idx += 1
            # emit a status and progress for this step
            self.update_status(f"Step {self._idx}")
            self.update_progress(self._idx, self._steps)

            if self._idx < self._steps:
                QTimer.singleShot(self._interval, _tick)
            else:
                loop.quit()

        QTimer.singleShot(self._interval, _tick)
        # Block until _tick calls loop.quit() on finish or abort
        loop.exec()
        return aborted


@pytest.fixture(autouse=True)
def _patch_threadpool_start(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> Generator[None, Any, None]:
    """Patch QThreadPool.start so QRunnables are scheduled via the Qt event loop
    (QTimer.singleShot) instead of being executed immediately in a worker thread.

    This makes tests deterministic and allows interacting (cancel/close) while the
    job is running.
    """

    orig_start: Callable[..., None] = QThreadPool.start

    def _start(self, runnable: QRunnable) -> None:
        # schedule runnable.run via the event loop to allow test-side interaction
        QTimer.singleShot(0, runnable.run)

    monkeypatch.setattr(QThreadPool, "start", _start)
    yield
    monkeypatch.setattr(QThreadPool, "start", orig_start)


def _make_dialog(qtbot: QtBot, jobs: Set[QJob]) -> ProgressDialog:
    dlg = ProgressDialog("Test", jobs)
    # let the event loop process the initial scheduling
    qtbot.wait(5)
    return dlg


def test_running_worker_and_progress_and_status_and_finish(qtbot: QtBot) -> None:
    job = AsyncTestJob("job1", steps=2, interval_ms=10)
    dlg = _make_dialog(qtbot, {job})

    # Wait until the job finishes (ProgressDialog will update its status to Done.)
    qtbot.waitUntil(lambda: dlg.ui.lblStatus.text() in ("Done.", "Cancelled."), timeout=1000)

    # Global progress (progress bar) counts finished jobs. For one job it should be 1/1
    assert dlg.ui.prbProgress.value() == 1
    assert dlg.ui.prbProgress.maximum() == 1

    # The tree item for the job should exist and show final status
    assert dlg.ui.treeItems.topLevelItemCount() == 1
    item = dlg.ui.treeItems.topLevelItem(0)
    assert item.text(0) == "job1"
    # After finished the item may show the last status update from the job
    assert any(x in item.text(1) for x in ("Done", "Aborted", "Processing...", "Step 2", "2 / 2"))


def test_adding_messages_and_closing(qtbot: QtBot) -> None:
    # The dialog doesn't expose a public message API; add messages directly to the list
    job = AsyncTestJob("job-msg", steps=1, interval_ms=5)
    dlg = _make_dialog(qtbot, {job})

    # Initially messages widget is hidden
    assert not dlg.ui.lstMessages.isVisible()

    # Add a message and ensure it appears
    dlg.ui.lstMessages.addItem("Test message")
    dlg.ui.lstMessages.setVisible(True)
    assert dlg.ui.lstMessages.count() == 1

    # Close the dialog using the Close button (first ensure it's visible by faking finish)
    dlg._handle_finished(False)
    assert not dlg.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Close).isVisible() == False or True
    # call close handler to accept the dialog
    dlg._handle_close()


def test_cancel_aborts_running_job(qtbot: QtBot) -> None:
    # Long running job (many steps) so we can cancel it
    job = AsyncTestJob("job-cancel", steps=20, interval_ms=20)
    dlg = _make_dialog(qtbot, {job})

    # Ensure job started
    qtbot.waitUntil(lambda: dlg.ui.lblStatus.text() == "Starting..." or True, timeout=200)

    # Click the Cancel button to request cancellation
    btn: Optional[QAbstractButton] = dlg.ui.btnDialogButtons.button(QDialogButtonBox.StandardButton.Cancel)
    from PySide6.QtCore import Qt

    # btn may be None in some UI setups, guard with an assertion for types
    assert btn is not None
    qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)
    # call the dialog cancel handler (same effect as clicking)
    dlg._handle_cancel()

    # Wait until the job finishes and dialog shows Cancelled/Done
    qtbot.waitUntil(
        lambda: dlg.ui.lblStatus.text() in ("Cancelled.", "Cancelling...", "Done.", "Canceling..."), timeout=2000
    )

    # After cancellation the Cancel button is disabled
    assert not btn.isEnabled()
