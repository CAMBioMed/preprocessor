from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from preprocessor.core.message_reporter import MessageReporter, NOOP_MESSAGE_REPORTER
from preprocessor.core.photo_params import PhotoParams
from preprocessor.core.progress_reporter import ProgressReporter, NOOP_PROGRESS_REPORTER
from preprocessor.core.types import ImageRGB


@dataclass(slots=True)
class ImageTransformWorkItem:
    """An image transformation work item."""

    image_id: str
    """Stable image ID."""
    image_path: Path
    """The original path to the image file."""
    image: ImageRGB
    """The image data as a numpy array."""
    params: PhotoParams
    """The parameters used for processing this image, e.g. quadrat corners."""


class ImageTransform(Protocol):
    """A callable that takes an image transform work item and returns a new work item."""

    name: str
    """The name of the transformation, displayed to the user and used for logging."""

    def __call__(
        self,
        item: ImageTransformWorkItem,
        /,
        *,
        messages: MessageReporter = NOOP_MESSAGE_REPORTER,
        progress: ProgressReporter = NOOP_PROGRESS_REPORTER,
    ) -> ImageTransformWorkItem:
        """Apply the transformation to the given work item and return the new work item.

        :param item: The work item to transform.
        :param messages: A message reporter for reporting messages during processing of this image.
        If not provided, a no-op message reporter will be used.
        :param progress: A progress reporter for reporting progress of processing steps.
        If not provided, a no-op progress reporter will be used.
        """
        ...
