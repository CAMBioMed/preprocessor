from PySide6.QtCore import QObject, Signal
from cv2.typing import Point2f


class PhotoModel(QObject):
    """
    The model for a single photo in the project.

    This includes photo-specific settings.
    """

    on_changed: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

    _quadrat_corners: tuple[Point2f, Point2f, Point2f, Point2f] | None = None
    on_quadrat_corners_changed: Signal = Signal()

    @property
    def quadrat_corners(self) -> tuple[Point2f, Point2f, Point2f, Point2f] | None:
        """The corners of the quadrat in the photo, if set."""
        return self._quadrat_corners

    @quadrat_corners.setter
    def quadrat_corners(self, value: tuple[Point2f, Point2f, Point2f, Point2f] | None) -> None:
        if self._quadrat_corners != value:
            self._quadrat_corners = value
            self.on_quadrat_corners_changed.emit()
            self.on_changed.emit()