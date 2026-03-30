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

def _clamp01(x: float) -> float:
    """Clamp a float to the range [0.0, 1.0].

    :param x: The float to clamp.
    :return: The clamped float.
    """
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x

class WeightedSubProgressReporter(ProgressReporter):
    """A progress reporter that combines multiple sub-progress reporters with weights."""

    _super: ProgressReporter
    _start: float
    _weight: float
    _image_id: str | None
    _step: str | None

    # PY-49246:
    # noinspection PyProtocol
    def __init__(
        self,
        super_reporter: ProgressReporter,
        start: float,
        weight: float,
        image_id: str | None = None,
        step: str | None = None,
    ) -> None:
        if start < 0.0 or start > 1.0:
            raise ValueError(f"Start must be between 0.0 and 1.0, got {start}")
        if weight < 0.0 or weight > 1.0:
            raise ValueError(f"Weight must be between 0.0 and 1.0, got {weight}")
        if start + weight > 1.0:
            raise ValueError(f"Start + weight must be <= 1.0, got {start} + {weight} = {start + weight}")

        self._super = super_reporter
        self._start = start
        self._weight = weight
        self._image_id = image_id
        self._step = step

    def __call__(self, progress: float, detail: str | None = None) -> None:
        overall = _clamp01(self._start + _clamp01(progress) * self._weight)
        self._super(overall, detail)