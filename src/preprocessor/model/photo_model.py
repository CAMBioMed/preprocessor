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

    _original_filename: str = ""
    on_original_filename_changed: Signal = Signal()

    @property
    def original_filename(self) -> str:
        """The original filename of the photo."""
        return self._original_filename

    @original_filename.setter
    def original_filename(self, value: str) -> None:
        if self._original_filename != value:
            self._original_filename = value
            self.on_original_filename_changed.emit()
            self.on_changed.emit()

    _metadata_filename: str = ""
    on_metadata_filename_changed: Signal = Signal()

    @property
    def metadata_filename(self) -> str:
        """The filename of the metadata file associated with the photo."""
        return self._metadata_filename

    @metadata_filename.setter
    def metadata_filename(self, value: str) -> None:
        if self._metadata_filename != value:
            self._metadata_filename = value
            self.on_metadata_filename_changed.emit()
            self.on_changed.emit()

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

    _red_shift: tuple[float, float] | None = None
    on_red_shift_changed: Signal = Signal()

    @property
    def red_shift(self) -> tuple[float, float] | None:
        """The red channel shift in (x, y) directions to correct chromatic aberration."""
        return self._red_shift

    @red_shift.setter
    def red_shift(self, value: tuple[float, float] | None) -> None:
        if self._red_shift != value:
            self._red_shift = value
            self.on_red_shift_changed.emit()
            self.on_changed.emit()

    _blue_shift: tuple[float, float] | None = None
    on_blue_shift_changed: Signal = Signal()

    @property
    def blue_shift(self) -> tuple[float, float] | None:
        """The blue channel shift in (x, y) directions to correct chromatic aberration."""
        return self._blue_shift

    @blue_shift.setter
    def blue_shift(self, value: tuple[float, float] | None) -> None:
        if self._blue_shift != value:
            self._blue_shift = value
            self.on_blue_shift_changed.emit()
            self.on_changed.emit()

    _camera_matrix: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]] | None = None
    on_camera_matrix_changed: Signal = Signal()

    @property
    def camera_matrix(self) -> tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]] | None:
        """3x3 camera matrix or None."""
        return self._camera_matrix

    @camera_matrix.setter
    def camera_matrix(self, value: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]] | None) -> None:
        if self._camera_matrix != value:
            self._camera_matrix = value
            self.on_camera_matrix_changed.emit()
            self.on_changed.emit()

    _distortion_coefficients: tuple[Point2f, ...] | None = None
    on_distortion_coefficients_changed: Signal = Signal()

    @property
    def distortion_coefficients(self) -> tuple[Point2f, ...] | None:
        """Sequence of distortion coefficients as Point2f or None."""
        return self._distortion_coefficients

    @distortion_coefficients.setter
    def distortion_coefficients(self, value: tuple[Point2f, ...] | None) -> None:
        if self._distortion_coefficients != value:
            self._distortion_coefficients = value
            self.on_distortion_coefficients_changed.emit()
            self.on_changed.emit()

    def serialize(self) -> dict:
        """
        Serialize this PhotoModel into basic Python types suitable for JSON.
        """
        qc = [[float(x), float(y)] for (x, y) in self.quadrat_corners] if self.quadrat_corners is not None else None
        rs = [float(self._red_shift[0]), float(self._red_shift[1])] if self._red_shift is not None else None
        bs = [float(self._blue_shift[0]), float(self._blue_shift[1])] if self._blue_shift is not None else None
        cm = [[float(v) for v in row] for row in self._camera_matrix] if self._camera_matrix is not None else None
        dc = [[float(x), float(y)] for (x, y) in self._distortion_coefficients] if self._distortion_coefficients is not None else None
        return {
            "original_filename": self._original_filename,
            "quadrat_corners": qc,
            "red_shift": rs,
            "blue_shift": bs,
            "camera_matrix": cm,
            "distortion_coefficients": dc,
        }

    def deserialize(self, data: dict) -> None:
        """
        Deserialize state from a dict produced by serialize.
        Uses the setters so signals are emitted only on change.
        If a key doesn't occur in the data, it is not set.
        """
        if "original_filename" in data:
            of = data.get("original_filename", "")
            if of is not None:
                if not isinstance(of, str):
                    raise ValueError("original_filename must be a string or None")
                self.original_filename = of
            else:
                # treat None as clearing to empty string
                self.original_filename = ""

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

        if "red_shift" in data:
            r = data.get("red_shift", None)
            if r is not None:
                try:
                    rs = (float(r[0]), float(r[1]))  # type: ignore[arg-type]
                except Exception:
                    raise ValueError("red_shift must be a pair of numbers or None")
                self.red_shift = rs
            else:
                self.red_shift = None

        if "blue_shift" in data:
            b = data.get("blue_shift", None)
            if b is not None:
                try:
                    bs = (float(b[0]), float(b[1]))  # type: ignore[arg-type]
                except Exception:
                    raise ValueError("blue_shift must be a pair of numbers or None")
                self.blue_shift = bs
            else:
                self.blue_shift = None

        if "camera_matrix" in data:
            cm_raw = data.get("camera_matrix", None)
            if cm_raw is not None:
                try:
                    cm_rows = [tuple(float(v) for v in row) for row in cm_raw]  # type: ignore[arg-type]
                except Exception:
                    raise ValueError("camera_matrix must be a 3x3 numeric structure or None")
                if len(cm_rows) != 3 or any(len(r) != 3 for r in cm_rows):
                    raise ValueError("camera_matrix must be 3x3")
                self.camera_matrix = (cm_rows[0], cm_rows[1], cm_rows[2])  # type: ignore[arg-type]
            else:
                self.camera_matrix = None

        if "distortion_coefficients" in data:
            d_raw = data.get("distortion_coefficients", None)
            if d_raw is not None:
                try:
                    dc = tuple((float(pt[0]), float(pt[1])) for pt in d_raw)  # type: ignore[arg-type]
                except Exception:
                    raise ValueError("distortion_coefficients must be a sequence of [x,y] pairs or None")
                self.distortion_coefficients = dc
            else:
                self.distortion_coefficients = None

