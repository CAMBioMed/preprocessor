from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Optional, Final, override


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

    def report_msg(self, message: Message) -> None:
        """Report a message.

        :param message: The message to report.
        """

    def report(
        self,
        level: MessageLevel,
        code: str,
        text: str,
        *,
        step: str | None = None,
        image_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report a message.

        :param level: The severity level of the message.
        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param step: The name of the processing step that generated this message, e.g. 'color_correction'.
        :param image_id: The stable image ID that this message pertains to, if applicable.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        self.report_msg(Message(level, code, text, step, image_id, details))

    def error(
        self,
        code: str,
        text: str,
        *,
        step: str | None = None,
        image_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report an error message to this work item.

        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param step: The name of the processing step that generated this message, e.g. 'color_correction'.
        :param image_id: The stable image ID that this message pertains to, if applicable.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        self.report(MessageLevel.error, code, text, step=step, image_id=image_id, details=details)

    def warn(
        self,
        code: str,
        text: str,
        *,
        step: str | None = None,
        image_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report a warning message to this work item.

        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param step: The name of the processing step that generated this message, e.g. 'color_correction'.
        :param image_id: The stable image ID that this message pertains to, if applicable.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        self.report(MessageLevel.warning, code, text, step=step, image_id=image_id, details=details)

    def info(
        self,
        code: str,
        text: str,
        *,
        step: str | None = None,
        image_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Report an info message.

        :param code: A machine-readable code for the message, e.g. 'color_correction_failed'.
        :param text: A human-readable message to be displayed to the user.
        :param step: The name of the processing step that generated this message, e.g. 'color_correction'.
        :param image_id: The stable image ID that this message pertains to, if applicable.
        :param details: Optional additional details about the message, for debugging or display purposes.
        """
        self.report(MessageLevel.info, code, text, step=step, image_id=image_id, details=details)


class NoopMessageReporter(MessageReporter):
    """A no-op implementation of MessageReporter that does nothing."""

    # Singleton instance holder
    _instance: Optional["NoopMessageReporter"] = None

    def __new__(cls) -> "NoopMessageReporter":
        """Ensure only one instance of NoopMessageReporter exists.

        Any attempt to construct the class will return the same shared
        instance. This simplifies usage and avoids unnecessary allocations
        for a stateless no-op reporter.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @override
    def report_msg(self, message: Message) -> None:
        # Intentionally do nothing (NOOP). We don't call the base
        # implementation because it is a no-op (ellipsis) and calling
        # super() is unnecessary here.
        return None


class CollectingMessageReporter(MessageReporter):
    """An implementation of MessageReporter that collects messages in a list."""

    _messages: list[Message]

    def __init__(self) -> None:
        self._messages: list[Message] = []

    @override
    def report_msg(self, message: Message) -> None:
        super().report_msg(message)
        self._messages.append(message)

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


# Module-level singleton of NoopMessageReporter
NOOP_MESSAGE_REPORTER: Final[NoopMessageReporter] = NoopMessageReporter()
