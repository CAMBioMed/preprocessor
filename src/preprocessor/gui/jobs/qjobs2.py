import threading
from threading import Event
from typing import override, cast

from PySide6.QtCore import QThreadPool, QObject, Signal, QRunnable, Slot, QTimer

from preprocessor.core.jobs.jobs import JobProcessor, Job, JobHandle, R, JobState, JobContext
from preprocessor.core.message_reporter import Message
from preprocessor.gui.jobs.qjobs import CancelToken, JobCancelledException


class QJobSignals(QObject):
    """Defines the signals available from a running job."""

    on_start: Signal = Signal(object)
    """Raised when a job starts. Emits (job: QJob)."""
    on_finished: Signal = Signal(object, object)
    """Raised when a job finishes. Emits (job: QJob, state: JobState, result: R | Exception | None)"""
    on_status: Signal = Signal(object, str)
    """Raised when a job updates its status. Emits (job: QJob, msg: str)"""
    on_state: Signal = Signal(object, object)
    """Raised when a job's state changes. Emits (job: QJob, state: JobState)"""
    on_progress: Signal = Signal(object, float)
    """Raised when a job updates its progress. Emits (job: QJob, progress: float)"""
    on_message: Signal = Signal(object, object)
    """Raised when a job reports a message. Emits (job: QJob, message: Message)"""


class QJob[R](QRunnable):
    """Wraps a Job to communicate with the UI via signals."""

    _job: Job[R]
    """The wrapped job."""
    _signals: QJobSignals
    """The signals used to communicate with the UI."""
    _state: JobState
    """The current state of the job."""
    _cancel_token: CancelToken
    """The cancellation token used to signal the job to stop."""
    _ctx: "QJobContext[R]"
    """The context passed to the job when running, providing cancellation and status update functionality."""

    def __init__(self, job: Job[R]) -> None:
        super().__init__()
        self._job = job
        self._signals = QJobSignals()
        self._state = JobState.PENDING
        self._cancel_token = CancelToken()
        self._ctx = QJobContext(self)

    @Slot()
    def run(self) -> None:
        try:
            self._state = JobState.RUNNING
            self._signals.on_start.emit(self)
            result = self._job.run(self._ctx)
            self._state = JobState.COMPLETED
            self._signals.on_finished.emit(self, JobState.COMPLETED, result)
        except JobCancelledException:
            self._state = JobState.CANCELLED
            self._signals.on_finished.emit(self, JobState.CANCELLED, None)
        except Exception as e:
            self._state = JobState.FAILED
            self._signals.on_finished.emit(self, JobState.FAILED, e)


# noinspection PyProtectedMember
class QJobContext[E](JobContext, JobHandle):
    """A JobContext implementation for QJob, providing cancellation and status update functionality."""

    _job: QJob
    _result: E | None
    _progress: float

    _finished_event: Event
    _finished_state: JobState | None
    _finished_result: object | None

    def __init__(self, job: QJob) -> None:
        self._job = job
        self._result = None
        self._progress = 0.0

        self._finished_event = threading.Event()
        self._finished_state = None
        self._finished_result = None

        self._job._signals.on_finished.connect(self._on_finished)

    @override
    def is_cancelled(self) -> bool:
        return self._job._cancel_token.is_cancelled()

    @override
    def update_status(self, message: str) -> None:
        self._job._signals.on_status.emit(self._job, message)

    @override
    def update_progress(self, progress: float) -> None:
        self._progress = progress
        self._job._signals.on_progress.emit(self._job, progress)

    @override
    def log_msg(self, message: Message) -> None:
        self._job._signals.on_message.emit(self._job, message)

    @override
    def run_subjob[R](self, job: "Job[R]", weight: float = 1.0) -> R:
        # Clamp weight to a sensible range
        weight = max(0.0, min(1.0, float(weight)))

        outer = self

        # Capture the parent's progress at the start so the child's progress is
        # reported in the range [parent_start, parent_start + weight].
        parent_start = outer._progress

        # The subcontext delegates to the outer context but maps progress into
        # the slice [parent_start .. parent_start + weight].
        class _SubContext(JobContext):
            def is_cancelled(self) -> bool:
                return outer.is_cancelled()

            def update_status(self, message: str) -> None:
                outer.update_status(message)

            def update_progress(self, progress: float) -> None:
                p = max(0.0, min(1.0, float(progress)))

                # Map child progress p into parent range [parent_start, parent_start + weight]
                scaled = parent_start + p * weight
                # Ensure we don't exceed the end of the allocated slice
                scaled = max(parent_start, min(parent_start + weight, scaled))
                outer.update_progress(scaled)

            def log_msg(self, message: Message) -> None:
                outer.log_msg(message)

            def run_subjob[R2](self, job2: "Job[R2]", weight2: float = 1.0) -> R2:
                # nested subjob: multiply weights so child progress is mapped correctly
                return outer.run_subjob(job2, weight * weight2)

        # Respect any cancellation requested before starting
        outer.check_cancelled()

        # Run sub-job synchronously in this thread, letting exceptions propagate
        result = job.run(_SubContext())

        # Check cancellation after completion too (sub-job may have been cancelled)
        outer.check_cancelled()

        # When subjob completes, ensure parent's progress reaches the end of the slice
        outer.update_progress(parent_start + weight)

        return result

    @override
    def state(self) -> JobState:
        return self._job._state

    @override
    def cancel(self) -> None:
        self._job._cancel_token.cancel()

    @override
    def await_result(self, timeout: float | None = None) -> E:
        finished = self._finished_event.wait(timeout)
        if not finished:
            raise TimeoutError("Timed out waiting for job result")

        return cast(E, self.try_result())

    @override
    def try_result(self) -> E | None:
        if not self._finished_event.is_set():
            return None

        if self._finished_state == JobState.COMPLETED:
            # type: ignore[return-value]
            return self._finished_result  # type: ignore
        elif self._finished_state == JobState.CANCELLED:
            raise JobCancelledException()
        elif self._finished_state == JobState.FAILED:
            if isinstance(self._finished_result, Exception):
                raise self._finished_result
            else:
                raise RuntimeError("Job failed with non-exception result")
        else:
            # fallback — shouldn't happen
            raise RuntimeError("Job finished in unexpected state")

    def _on_finished(self, job: QJob, state: JobState, result: object) -> None:
        # Capture final state and result, and wake waiters
        self._finished_state = state
        self._finished_result = result
        self._finished_event.set()


# noinspection PyProtectedMember
class QJobProcessor(QObject, JobProcessor):

    _pool: QThreadPool
    """The thread pool used to run the jobs."""
    _cancel_token: CancelToken
    """A cancellation token that can be used to signal jobs to stop."""
    _run_in_thread: bool
    """Whether to run jobs on a separate thread instead of on the Qt event loop."""

    _qjobs: list[QJob]

    on_job_start: Signal = Signal(object)
    """Raised when a job starts. Emits (job: QJob)."""
    on_job_finished: Signal = Signal(object, object)
    """Raised when a job finishes. Emits (job: QJob, state: JobState, result: R | Exception | None)"""
    on_job_status: Signal = Signal(object, str)
    """Raised when a job updates its status. Emits (job: QJob, msg: str)"""
    on_job_state: Signal = Signal(object, object)
    """Raised when a job's state changes. Emits (job: QJob, state: JobState)"""
    on_job_progress: Signal = Signal(object, float)
    """Raised when a job updates its progress. Emits (job: QJob, progress: float)"""
    on_job_message: Signal = Signal(object, object)
    """Raised when a job reports a message. Emits (job: QJob, message: Message)"""

    def __init__(self, parent: QObject | None = None, run_in_thread: bool = True):
        """
        Creates a QJobProcessor.

        :param parent: The parent QObject for this processor, used for signal/slot connections and thread affinity.
        :param run_in_thread: Whether to run jobs in a separate thread. If False, jobs will run on the Qt event loop.
        This is mainly used so that tests can run jobs deterministically on the main thread.
        """
        super().__init__(parent)
        self._cancel_token = CancelToken()
        self._run_in_thread = run_in_thread
        self._qjobs = []

    @override
    def cancel_all(self) -> None:
        for qjob in self._qjobs:
            qjob._cancel_token.cancel()

    @override
    def submit(self, job: Job[R]) -> JobHandle[R]:
        qjob = QJob(job)
        self._qjobs.append(qjob)
        if self._run_in_thread:
            self._pool.start(qjob)
        else:
            # Schedule runnable.run on the Qt event loop for deterministic execution
            QTimer.singleShot(0, job.run)
        return qjob._ctx