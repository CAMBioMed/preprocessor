from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class MessageLevel(StrEnum):
    """Specifies the severity level of a message."""

    info = "info"
    warning = "warning"
    error = "error"


@dataclass(frozen=True, slots=True)
class Message:
    level: MessageLevel
    """The severity level of the message."""
    code: str
    """A machine-readable code for the message, e.g. 'color_correction_failed'."""
    text: str
    """A human-readable message to be displayed to the user."""
    step: str | None = None
    """The name of the processing step that generated this message, e.g. 'color_correction'."""
    image_id: str | None = None
    """The stable image ID that this message pertains to, if applicable."""
    details: dict[str, Any] | None = None
    """Optional additional details about the message, for debugging or display purposes."""
