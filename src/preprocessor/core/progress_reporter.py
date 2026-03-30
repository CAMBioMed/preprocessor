from typing import Protocol


class ProgressReporter(Protocol):
    """Protocol for reporting progress of image processing steps."""

    def __call__(self, progress: float, detail: str | None = None, /) -> None:
        """Report progress of a processing step for an image.

        :param progress: A float between 0.0 and 1.0 indicating the progress of the step.
        :param detail: Optional additional details about the step.
        """
        ...


class NoopProgressReporter(ProgressReporter):
    """A no-op implementation of ProgressReporter that does nothing."""

    def __call__(self, progress: float, detail: str | None = None) -> None:
        pass
