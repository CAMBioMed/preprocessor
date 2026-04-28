import threading
from abc import ABC, abstractmethod, abstractproperty
from threading import Event
from typing import override, cast

from PySide6.QtCore import QThreadPool, QObject, Signal, QRunnable, Slot, QTimer

from preprocessor.core.jobs.jobs import JobProcessor, Job, JobHandle, R, JobState, JobContext, CancelToken, \
    JobCancelledException
from preprocessor.core.message_reporter import Message



class QJobSignals(QObject):
    """Defines the signals available from a running job."""

    on_start: Signal = Signal(object)
    """Raised when a job starts. Emits (job: QJob)."""
    on_finished: Signal = Signal(object, object, object)
    """Raised when a job finishes. Emits (job: QJob, state: JobState, result: R | Exception | None)"""
    on_status: Signal = Signal(object, str)
    """Raised when a job updates its status. Emits (job: QJob, msg: str)"""
    on_state: Signal = Signal(object, object)
    """Raised when a job's state changes. Emits (job: QJob, state: JobState)"""
    on_progress: Signal = Signal(object, float)
    """Raised when a job updates its progress. Emits (job: QJob, progress: float)"""
    on_message: Signal = Signal(object, object)
    """Raised when a job reports a message. Emits (job: QJob, message: Message)"""


class QJob[R](QRunnable, ABC):

    signals: QJobSignals
    """The signals used to communicate with the UI."""
    _ctx: "QJobContext[R]"
    """The context passed to the job when running, providing cancellation and status update functionality."""

    def __init__(self, job: Job[R]) -> None:
        super().__init__()
        self._job = job
        self.signals = QJobSignals()
        self._ctx = QJobContext(self)

    @abstractmethod
    def execute(self, ctx: "QJobContext[R]") -> R:
        """Run the job and return its result.

        :param ctx: The context for running the job, providing necessary services
        and information such as cancellation status, progress reporting, and message reporting.
        :return: The result of the job, which can be any object depending on the job.
        :raises JobCancelledException: If cancellation is requested during the job.
        """
        ...


    @Slot()
    def run(self) -> None:
        try:
            self._state = JobState.RUNNING
            self.signals.on_start.emit(self)
            result = self.execute(self._ctx)
            self._state = JobState.COMPLETED
            self.signals.on_finished.emit(self, JobState.COMPLETED, result)
        except JobCancelledException:
            self._state = JobState.CANCELLED
            self.signals.on_finished.emit(self, JobState.CANCELLED, None)
        except Exception as e:
            self._state = JobState.FAILED
            self.signals.on_finished.emit(self, JobState.FAILED, e)


class QJobOfJob[R](QJob[R]):
    """Wraps a Job to communicate with the UI via signals."""

    _job: Job[R]
    """The wrapped job."""
    signals: QJobSignals
    """The signals used to communicate with the UI."""
    _ctx: "QJobContext[R]"
    """The context passed to the job when running, providing cancellation and status update functionality."""

    def __init__(self, job: Job[R]) -> None:
        super().__init__()
        self._job = job
        self.signals = QJobSignals()
        self._ctx = QJobContext(self)

    @Slot()
    def run(self) -> None:
        try:
            self._state = JobState.RUNNING
            self.signals.on_start.emit(self)
            result = self._job.execute(self._ctx)
            self._state = JobState.COMPLETED
            self.signals.on_finished.emit(self, JobState.COMPLETED, result)
        except JobCancelledException:
            self._state = JobState.CANCELLED
            self.signals.on_finished.emit(self, JobState.CANCELLED, None)
        except Exception as e:
            self._state = JobState.FAILED
            self.signals.on_finished.emit(self, JobState.FAILED, e)


class QJobHandle[E](JobHandle[E], ABC):

    @property
    @abstractmethod
    def signals(self) -> QJobSignals:
        """The signals emitted by the job, for monitoring progress and status."""
        ...

    @property
    @abstractmethod
    def job(self) -> QJob:
        """The underlying QJob instance."""
        ...

# noinspection PyProtectedMember
class QJobContext[R](JobContext, QJobHandle):
    """A JobContext implementation for QJob, providing cancellation and status update functionality."""

    _job: QJob
    """The QJob being run."""
    _result: R | Exception | None
    """The current result of the job, if available. Only set when the job finishes successfully."""
    _progress: float
    """The current progress of the job, as a value between 0.0 and 1.0."""
    _state: JobState
    """The current state of the job."""
    _cancel_token: CancelToken
    """The cancellation token used to signal the job to stop."""
    _finished_event: Event
    """An event that is set when the job finishes, allowing await_result to wait for completion."""

    def __init__(self, job: QJob) -> None:
        self._job = job
        self._result = None
        self._progress = 0.0
        self._state = JobState.PENDING
        self._cancel_token = CancelToken()
        self._finished_event = threading.Event()

        self._job.signals.on_finished.connect(self._on_finished)

    @property
    @override
    def signals(self) -> QJobSignals:
        """The signals emitted by the job, for monitoring progress and status."""
        return self._job.signals

    @property
    @override
    def job(self) -> QJob:
        """The underlying QJob instance."""
        return self._job

    @override
    def is_cancelled(self) -> bool:
        return self._cancel_token.is_cancelled()

    @override
    def update_status(self, message: str) -> None:
        self._job.signals.on_status.emit(self._job, message)

    @override
    def update_progress(self, progress: float) -> None:
        self._progress = progress
        self._job.signals.on_progress.emit(self._job, progress)

    @override
    def log_msg(self, message: Message) -> None:
        self._job.signals.on_message.emit(self._job, message)

    @override
    def run_subjob[R2](self, job: "Job[R2]", weight: float = 1.0) -> R2:
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

            def run_subjob[R3](self, job2: "Job[R3]", weight2: float = 1.0) -> R3:
                # nested subjob: multiply weights so child progress is mapped correctly
                return outer.run_subjob(job2, weight * weight2)

        # Respect any cancellation requested before starting
        outer.check_cancelled()

        # Run sub-job synchronously in this thread, letting exceptions propagate
        result = job.execute(_SubContext())

        # Check cancellation after completion too (sub-job may have been canceled)
        outer.check_cancelled()

        # When subjob completes, ensure parent's progress reaches the end of the slice
        outer.update_progress(parent_start + weight)

        return result

    @override
    def state(self) -> JobState:
        return self._state

    @override
    def cancel(self) -> None:
        self._cancel_token.cancel()

    @override
    def await_result(self, timeout: float | None = None) -> R:
        finished = self._finished_event.wait(timeout)
        if not finished:
            raise TimeoutError("Timed out waiting for job result")

        return cast(R, self.try_result())

    @override
    def try_result(self) -> R | None:
        if not self._finished_event.is_set():
            return None

        if self._state == JobState.COMPLETED:
            # type: ignore[return-value]
            return self._result  # type: ignore
        elif self._state == JobState.CANCELLED:
            raise JobCancelledException()
        elif self._state == JobState.FAILED:
            if isinstance(self._result, Exception):
                raise self._result
            else:
                raise RuntimeError("Job failed with non-exception result")
        else:
            # fallback — shouldn't happen
            raise RuntimeError("Job finished in unexpected state")

    def _on_finished(self, job: QJob, state: JobState, result: object) -> None:
        # Capture final state and result, and wake waiters
        self._state = state
        self._result = result
        self._finished_event.set()

# Create a metaclass that is compatible with both QObject (from PySide6) and JobProcessor (ABC)
class QJobProcessorMeta(type(QObject), type(JobProcessor)):
    """Metaclass to allow QJobProcessor to inherit from both QObject and JobProcessor."""
    pass


# noinspection PyProtectedMember
class QJobProcessor(QObject, JobProcessor, metaclass=QJobProcessorMeta):

    _pool: QThreadPool
    """The thread pool used to run the jobs."""
    _cancel_token: CancelToken
    """A cancellation token that can be used to signal jobs to stop."""
    _run_in_thread: bool
    """Whether to run jobs on a separate thread instead of on the Qt event loop."""

    _qjobs: list[tuple[QJob, QJobHandle]]
    """The currently running QJobs and their associated handles, so they can be cancelled if needed."""

    on_job_start: Signal = Signal(object)
    """Raised when a job starts. Emits (job: QJob)."""
    on_job_finished: Signal = Signal(object, object, object)
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
        # Ensure a thread pool is available when running in threads
        self._pool = QThreadPool.globalInstance()

        # Prepare job signal forwarding helpers

    def _connect_job_signals(self, qjob: QJob) -> None:
        # Ensure the job uses the processor's cancel token
        qjob._cancel_token = self._cancel_token

        # Forward signals from the QJob to the processor's signals
        qjob.signals.on_start.connect(self._handle_job_start)
        qjob.signals.on_finished.connect(self._handle_job_finished)
        qjob.signals.on_status.connect(self._handle_job_status)
        qjob.signals.on_progress.connect(self._handle_job_progress)
        qjob.signals.on_message.connect(self._handle_job_message)

    def _handle_job_start(self, job: QJob) -> None:
        self.on_job_start.emit(job)

    def _handle_job_finished(self, job: QJob, state: JobState, result: object) -> None:
        self._qjobs.remove(job)
        self.on_job_finished.emit(job, state, result)

    def _handle_job_status(self, job: QJob, msg: str) -> None:
        self.on_job_status.emit(job, msg)

    def _handle_job_progress(self, job: QJob, progress: float) -> None:
        self.on_job_progress.emit(job, progress)

    def _handle_job_message(self, job: QJob, message: Message) -> None:
        self.on_job_message.emit(job, message)

    @override
    def cancel_all(self) -> None:
        for qjob in self._qjobs:
            qjob._cancel_token.cancel()

    @override
    def submit_job(self, job: Job[R]) -> QJobHandle[R]:
        qjob = QJobOfJob(job)
        return self.submit_qjob(qjob)

    def submit_qjob(self, qjob: QJob[R]) -> QJobHandle[R]:
        """Submit a QJob directly, without wrapping it in a Job. This is used when the caller already has a QJob instance."""
        self._qjobs.append(qjob)
        self._connect_job_signals(qjob)
        if self._run_in_thread:
            self._pool.start(qjob)
        else:
            # Run synchronously on the calling thread for deterministic execution
            # (tests use this path to avoid depending on the Qt event loop)
            qjob.run()
        return qjob._ctx