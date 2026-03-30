from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, Any


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


class MessageReporter:
    """Class handling reporting messages (info, warnings, errors) during image processing steps."""

    _step: str | None
    _image_id: str | None
    _has_errors: bool = False
    _has_warnings: bool = False
    _has_infos: bool = False

    def __init__(self, step: str | None = None, image_id: str | None = None) -> None:
        self._step = step
        self._image_id = image_id

    def report(
        self,
        level: MessageLevel,
        code: str,
        text: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report a message.

        :param level: The severity level of the message.
        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        if level == MessageLevel.error:
            self._has_errors = True
        elif level == MessageLevel.warning:
            self._has_warnings = True
        elif level == MessageLevel.info:
            self._has_infos = True

    def error(
        self,
        code: str,
        text: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report an error message to this work item.

        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        self.report(MessageLevel.error, code, text, details)

    def warn(
        self,
        code: str,
        text: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report a warning message to this work item.

        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        self.report(MessageLevel.warning, code, text, details)

    def info(
        self,
        code: str,
        text: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report an info message.

        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        self.report(MessageLevel.info, code, text, details)

    @property
    def has_errors(self) -> bool:
        """Whether any error messages have been collected."""
        return self._has_errors

    @property
    def has_warnings(self) -> bool:
        """Whether any warning messages have been collected."""
        return self._has_warnings

    @property
    def has_infos(self) -> bool:
        """Whether any info messages have been collected."""
        return self._has_infos

class NoopMessageReporter(MessageReporter):
    """A no-op implementation of MessageReporter that does nothing."""

    def report(
        self,
        level: MessageLevel,
        code: str,
        text: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().report(level, code, text, details)
        # Nothing else to do: NOOP

class CollectingMessageReporter(MessageReporter):
    """An implementation of MessageReporter that collects messages in a list."""

    _messages: list[Message]

    def __init__(self, step: str | None, image_id: str | None) -> None:
        super().__init__(step, image_id)
        self._messages: list[Message] = []

    def report(
        self,
        level: MessageLevel,
        code: str,
        text: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().report(level, code, text, details)
        msg = Message(
            level=level,
            code=code,
            text=text,
            step=self._step,
            image_id=self._image_id,
            details=details,
        )
        self._messages.append(msg)

    @property
    def messages(self) -> list[Message]:
        """A list of all collected messages."""
        return self._messages

    @property
    def errors(self) -> list[Message]:
        """A list of collected error messages."""
        return [msg for msg in self.messages if msg.level == MessageLevel.error]

    @property
    def warnings(self) -> list[Message]:
        """A list of collected warning messages."""
        return [msg for msg in self.messages if msg.level == MessageLevel.warning]

    @property
    def infos(self) -> list[Message]:
        """A list of collected info messages."""
        return [msg for msg in self.messages if msg.level == MessageLevel.info]

    @property
    def has_errors(self) -> bool:
        """Whether any error messages have been collected."""
        return any(msg.level == MessageLevel.error for msg in self.messages)

    @property
    def has_warnings(self) -> bool:
        """Whether any warning messages have been collected."""
        return any(msg.level == MessageLevel.warning for msg in self.messages)

    @property
    def has_infos(self) -> bool:
        """Whether any info messages have been collected."""
        return any(msg.level == MessageLevel.info for msg in self.messages)
