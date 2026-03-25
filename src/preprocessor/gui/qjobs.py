from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QThreadPool
from PySide6.QtGui import QIcon


from threading import Event

class CancelToken:
    """A simple cancellation token that can be shared between threads to signal when a job should be canceled."""
    def __init__(self) -> None:
        self._event = Event()

    def cancel(self) -> None:
        self._event.set()

    def is_cancelled(self) -> bool:
        return self._event.is_set()

class QJobSignals(QObject):
    """Defines the signals available from a running job."""

    on_job_start: Signal = Signal(object)
    """Raised when the job starts. Emits: (self: QJob)"""
    on_job_end: Signal = Signal(object, bool)
    """Raised when the job ends. Emits: (self: QJob, aborted: bool)"""
    on_job_progress: Signal = Signal(object, int, int)
    """Raised to report job progress. Emits: (self: QJob, steps: int, total: int)"""
    on_job_status: Signal = Signal(object, str, object)
    """Raised to report job status change. Emits: (self: QJob, new_status: str, icon: QIcon | str | None)"""


class QJob(QRunnable):
    """A QRunnable that performs a task in the background and communicates with the UI via signals."""

    name: str
    """The name of the job, used for display purposes."""
    signals: QJobSignals
    """The signals used to communicate with the UI."""
    cancel_token: CancelToken | None
    """An optional cancellation token that can be used to signal the job to stop."""

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.signals = QJobSignals()
        self.cancel_token = CancelToken()

    @Slot()
    def run(self) -> None:
        aborted = False
        try:
            self.signals.on_job_start.emit(self)
            aborted = self.process()
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            aborted = True
        finally:
            self.signals.on_job_end.emit(self, aborted)

    def process(self) -> bool:
        """Override this method with the job's task.
        This method will be called in the background thread.

        :return: True if the job was aborted, False otherwise.
        """
        return False

    def update_progress(self, steps: int, total_steps: int) -> None:
        """Call this method to update the job's progress."""
        self.signals.on_job_progress.emit(self, steps, total_steps)

    def update_status(self, status: str) -> None:
        """Call this method to update the job's status."""
        self.signals.on_job_status.emit(self, status, None)


class QJobProcessor(QObject):

    _pool: QThreadPool
    """The thread pool used to run the jobs."""
    _jobs: set[QJob]
    """The set of jobs being processed."""
    _finished: int
    """The number of finished jobs."""
    total: int
    """The total number of jobs."""
    _any_aborted: bool
    """Whether any job was aborted."""
    _cancel_token: CancelToken | None
    """An optional cancellation token that can be used to signal jobs to stop."""

    on_started: Signal = Signal()
    """Signal when processing starts."""
    on_progress: Signal = Signal(int, int)
    """Signal processing progress: processed, total"""
    on_status: Signal = Signal(str)
    """Signal a processing status change: new status."""
    on_finished: Signal = Signal(bool)
    """Signal when processing is finished."""

    on_job_start: Signal = Signal(object)
    """Raised when the job starts. Emits the QJob instance."""
    on_job_end: Signal = Signal(object, bool)
    """Raised when the job ends. Emits (QJob, aborted: bool)."""
    on_job_status: Signal = Signal(object, str, object)
    """Signal a job status update: QJob, new item status, new item icon (QIcon | str | None)"""
    on_job_progress: Signal = Signal(object, int, int)
    """Signal job progress: QJob, steps, total steps."""

    def __init__(self, jobs: set[QJob], parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._pool = QThreadPool.globalInstance()
        self._jobs = jobs
        self._finished = 0
        self.total = len(jobs)
        self._any_aborted = False
        self._cancel_token = CancelToken()

        for job in jobs:
            self._connect_job_signals(job)

    def _connect_job_signals(self, job: QJob) -> None:
        # Ensure we're all using the same cancel token here
        job.cancel_token = self._cancel_token

        # Connect signals in a way that is tolerant to different signal signatures
        job.signals.on_job_start.connect(self._handle_job_start)
        job.signals.on_job_end.connect(self._handle_job_end)
        job.signals.on_job_status.connect(self._handle_job_status)
        job.signals.on_job_progress.connect(self._handle_job_progress)

    def start(self) -> None:
        """Start processing the jobs."""
        self.on_started.emit()
        for job in self._jobs:
            self._pool.start(job)

    def cancel(self) -> None:
        """Request cancellation of all jobs."""
        self._cancel_token.cancel()

    def _handle_job_start(self, job: QJob) -> None:
        self.on_job_start.emit(job)

    def _handle_job_end(self, job: QJob, aborted: bool) -> None:
        self._finished += 1
        self._any_aborted = self._any_aborted or aborted
        self.on_job_end.emit(job, aborted)
        self.update_progress()
        if self._finished == self.total:
            self.on_finished.emit(self._any_aborted)

    def _handle_job_status(self, job: QJob, status: str, icon: object) -> None:
        self.on_job_status.emit(job, status, icon)

    def _handle_job_progress(self, job: QJob, steps: int, total_steps: int) -> None:
        self.on_job_progress.emit(job, steps, total_steps)

    def update_progress(self) -> None:
        self.on_progress.emit(self._finished, self.total)
