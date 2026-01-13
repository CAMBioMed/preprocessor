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

    def serialize(self) -> dict:
        """
        Serialize this PhotoModel into basic Python types suitable for JSON.
        """
        qc = [[float(x), float(y)] for (x, y) in self.quadrat_corners] if self.quadrat_corners is not None else None
        return {
            "quadrat_corners": qc,
        }

    def deserialize(self, data: dict) -> None:
        """
        Deserialize state from a dict produced by serialize.
        Uses the setters so signals are emitted only on change.
        If a key doesn't occur in the data, it is not set.
        """
        if "quadrat_corners" in data:
            qcs = data.get("quadrat_corners", None)
            if qcs is not None:
                # Expecting iterable of 4 [x, y] pairs
                qc = tuple((float(pt[0]), float(pt[1])) for pt in qcs)  # type: ignore[arg-type]
                if len(qc) != 4:
                    raise ValueError("quadrat_corners must contain 4 points")
                self.quadrat_corners = qc
            else:
                self.quadrat_corners = None

