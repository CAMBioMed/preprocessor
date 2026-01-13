from PySide6.QtCore import QObject, Signal


class PhotoModel(QObject):
    """
    The model for a single photo in the project.

    This includes photo-specific settings.
    """

    on_changed: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()
