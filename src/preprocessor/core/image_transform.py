from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Protocol, Any

from preprocessor.core.messages import Message, MessageLevel
from preprocessor.core.photo_params import PhotoParams
from preprocessor.core.types import Image, ImageRGB


@dataclass(slots=True)
class ImageTransformWorkItem:
    """
    An image transformation work item.
    """
    image_id: str
    """Stable image ID."""
    image_path: Path
    """The original path to the image file."""
    image: ImageRGB
    """The image data as a numpy array."""
    params: PhotoParams
    """The parameters used for processing this image, e.g. quadrat corners."""
    messages: list[Message] = field(default_factory=list)

    def add_message(self, level: MessageLevel, code: str, text: str, step: str | None = None, details: dict[str, Any] | None = None) -> None:
        """Add a message to this work item."""
        msg = Message(
            level=level,
            code=code,
            text=text,
            step=step,
            image_id=self.image_id,
            details=details,
        )
        self.messages.append(msg)

    def info(self, code: str, text: str, step: str | None = None, details: dict[str, Any] | None = None) -> None:
        """Add an info message to this work item."""
        self.add_message(MessageLevel.info, code, text, step, details)

    def warn(self, code: str, text: str, step: str | None = None, details: dict[str, Any] | None = None) -> None:
        """Add a warning message to this work item."""
        self.add_message(MessageLevel.warning, code, text, step, details)

    def error(self, code: str, text: str, step: str | None = None, details: dict[str, Any] | None = None) -> None:
        """Add an error message to this work item."""
        self.add_message(MessageLevel.error, code, text, step, details)


class ImageTransform(Protocol):
    """A callable that takes an image transform work item and returns a new work item."""

    name: str
    """The name of the transformation, displayed to the user and used for logging."""

    def __call__(self, item: ImageTransformWorkItem, /) -> ImageTransformWorkItem:
        """Apply the transformation to the given work item and return the new work item."""
        ...
