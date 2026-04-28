from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

from preprocessor.core.message_reporter import Message, MessageLevel
from preprocessor.gui.jobs.qjobs import JobCancelledException
from enum import Enum, auto

R = TypeVar("R")

class JobContext(ABC):
    """Context for running a job, providing necessary services and information.

    This class can be extended to include additional context information as needed.
    """

    @abstractmethod
    def is_cancelled(self) -> bool:
        """Return whether cancellation has been requested for the job."""
        ...

    def check_cancelled(self) -> None:
        """Check if cancellation has been requested, and if so, raise JobCancelledException."""
        if self.is_cancelled():
            raise JobCancelledException()

    @abstractmethod
    def update_status(self, message: str) -> None:
        """Update the status message for the job, which can be displayed to the user.

        Updating the status message replaces any previous status message.
        """
        ...

    @abstractmethod
    def update_progress(self, progress: float) -> None:
        """Update the progress of the job.

        :param progress: A number representing the current progress of the job, between 0.0 and 1.0.
        """
        ...

    @abstractmethod
    def log_msg(self, message: Message) -> None:
        """Report a message.

        :param message: The message to report.
        """
        ...

    def log(
        self,
        level: MessageLevel,
        code: str,
        text: str,
        *,
        step: str | None = None,
        subject: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report a message.

        :param level: The severity level of the message.
        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param step: The name of the processing step that generated this message, e.g. 'color_correction'.
        :param subject: The subject that this message pertains to, if applicable. For example, an image ID or path.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        self.log_msg(Message(level, code, text, step, subject, details))

    def log_error(
        self,
        code: str,
        text: str,
        *,
        step: str | None = None,
        subject: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report an error message to this work item.

        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param step: The name of the processing step that generated this message, e.g. 'color_correction'.
        :param subject: The subject that this message pertains to, if applicable. For example, an image ID or path.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        self.log(MessageLevel.error, code, text, step=step, subject=subject, details=details)

    def log_warn(
        self,
        code: str,
        text: str,
        *,
        step: str | None = None,
        subject: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report a warning message to this work item.

        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param step: The name of the processing step that generated this message, e.g. 'color_correction'.
        :param subject: The subject that this message pertains to, if applicable. For example, an image ID or path.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        self.log(MessageLevel.warning, code, text, step=step, subject=subject, details=details)

    def log_info(
        self,
        code: str,
        text: str,
        *,
        step: str | None = None,
        subject: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report an info message.

        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param step: The name of the processing step that generated this message, e.g. 'color_correction'.
        :param subject: The subject that this message pertains to, if applicable. For example, an image ID or path.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        self.log(MessageLevel.info, code, text, step=step, subject=subject, details=details)

    @abstractmethod
    def run_subjob[R](self, job: "Job[R]", weight: float = 1.0) -> R:
        """Run a child job within this job's context.

        This method can be used to run another job as part of this job's execution, while still respecting
        the cancellation status and allowing the sub-job to report messages and progress through this context.

        :param job: The sub-job to run.
        :param weight: The weight of the sub-job's progress within the overall progress,
        as a float between 0.0 and 1.0.
        :return: The result of the sub-job.
        :raises JobCancelledException: If cancellation is requested during the sub-job.
        """
        ...


class Job(ABC, Generic[R]):
    """Base class for jobs.

    Each job should implement the run method to perform the job's action and return results.
    """

    name: str
    """Name of the job, displayed to the user and used for logging."""

    @abstractmethod
    def run(
        self,
        ctx: JobContext,
     ) -> R:
        """Run the job and return its result.

        :param ctx: The context for running the job, providing necessary services
        and information such as cancellation status, progress reporting, and message reporting.
        :return: The result of the job, which can be any object depending on the job.
        :raises JobCancelledException: If cancellation is requested during the job.
        """
        ...


class JobState(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()

class JobHandle(ABC, Generic[R]):

    @abstractmethod
    def state(self) -> JobState:
        """Get the current state of the job."""
        ...

    def is_running(self) -> bool:
        """Return whether the job is currently running."""
        return self.state() == JobState.RUNNING

    def is_done(self) -> bool:
        """Return whether the job is done (completed, failed, or canceled)."""
        return self.state() in {JobState.COMPLETED, JobState.FAILED, JobState.CANCELLED}

    @abstractmethod
    def cancel(self) -> None:
        """Request cancellation of the job."""
        ...

    @abstractmethod
    def await_result(self, timeout: float | None = None) -> R:
        """Blocks the thread waiting for the job to complete and return its result.

        :param timeout: Optional timeout in seconds to wait for the job to complete.
        If None, wait indefinitely.
        :return: The result of the job.
        :raises TimeoutError: If the timeout is reached before the job completes.
        :raises JobCancelledException: If the job was canceled before completion.
        :raises Exception: If the job failed with an exception during execution.
        """
        ...

    @abstractmethod
    def try_result(self) -> R | None:
        """Try to get the result of the job without blocking.

        :return: The result of the job if it is completed, or None if the job is still running.
        :raises JobCancelledException: If the job was canceled before completion.
        :raises Exception: If the job failed with an exception during execution.
        """
        ...

class JobProcessor(ABC):
    """A class responsible for processing jobs."""

    @abstractmethod
    def submit[R](self, job: Job[R]) -> JobHandle[R]:
        """Submit a job for processing.

        :param job: The job to process.
        :return: A handle to the submitted job, which can be used to track its progress,
        cancel the job, and get its result.
        """
        ...

    @abstractmethod
    def cancel_all(self) -> None:
        """Reqquest cancellation of all jobs."""
        ...