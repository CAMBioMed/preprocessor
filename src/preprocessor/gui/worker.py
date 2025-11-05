import logging
import sys
import traceback
from typing import Callable, Any

from PySide6.QtCore import Slot, QRunnable, Signal, QObject

from PySide6.QtCore import QThreadPool

logger = logging.getLogger(__name__)

# Based on: https://www.pythonguis.com/tutorials/multithreading-pyside6-applications-qthreadpool/

class WorkerManager:
    """Manages a pool of worker threads to run tasks in the background."""

    def __init__(self):
        # Note sure what the trade-off is between using QThreadPool.globalInstance() vs creating a new QThreadPool().
        self.threadpool = QThreadPool.globalInstance()

    def start(self, worker: QRunnable):
        """Start a worker in the thread pool."""
        # By default, the threadpool will take ownership of the worker
        # and (as autoDelete is enabled) clean it up when done.
        # However, signals seem to not be emitted when autoDelete is True.
        # This comment https://github.com/git-cola/git-cola/blob/1b9279dd937c9f4db0273c5ffee955231b668e8d/cola/qtutils.py#L1156-L1159
        # indicates that this is due to Python performing double-free,
        # so we disable Qt auto-deletion here and let Python clean the worker up.
        worker.setAutoDelete(False)
        self.threadpool.start(worker)


class WorkerSignals(QObject):
    """Defines the signals available from a running worker thread."""

    progress = Signal(float)
    """Signal for reporting progress as a float between 0 (0%) and 1 (100%)."""
    finished = Signal()
    """Signals when the worker has finished."""
    result = Signal(object)
    """Signals when the worker has a result to return."""
    error = Signal(tuple)
    """Signals when an error occurred. Emits a tuple of (exctype, value, traceback)."""


class Worker(QRunnable):
    """
    A worker for running tasks in the background.

    Usage:
        def my_task(progress_callback):
            for i in range(100):
                # do work...
                progress_callback(i / 100)
            return result

        worker = Worker(my_task)
        worker.signals.result.connect(handle_result)
        worker.signals.progress.connect(handle_progress)
        worker.signals.finished.connect(handle_finished)
        worker.signals.error.connect(handle_error)

        worker_manager.start(worker)
    """

    fn: Callable
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    signals: WorkerSignals

    def __init__(self, fn: Callable, *args, **kwargs):
        """
        :param fn: The task (callable) to run in the background.
        :param args: Positional arguments for the task.
        :param kwargs: Keyword arguments for the task.
        """
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # Add the progress callback to the kwargs
        self.kwargs["progress_callback"] = self.signals.progress

    @Slot()
    def run(self):
        try:
            logger.debug("Starting worker task.")
            result = self.fn(*self.args, **self.kwargs)
            logger.debug("Worker task completed.")
        except Exception as e:
            logger.error("Error in worker task: %s", e)
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            logger.debug("Emitting result from worker task.")
            self.signals.result.emit(result)
        finally:
            logger.debug("Emitting finished signal from worker task.")
            self.signals.finished.emit()
