from pathlib import Path
from typing import Any, cast

from PySide6.QtCore import Signal
from cv2.typing import Point2f
from pydantic import BaseModel, field_validator

from preprocessor.model.camera_model import CameraMatrix
from preprocessor.model.qmodel import QModel


class PhotoData(BaseModel):
    """The data for a single photo in the project, used for serialization."""

    original_filename: Path | None = None
    """The original path to the photo file, if set."""
    quadrat_corners: list[Point2f] = []
    """The corners of the quadrat in the photo, if set."""
    red_shift: tuple[float, float] | None = None
    """The red channel shift in (x, y) directions to correct chromatic aberration."""
    blue_shift: tuple[float, float] | None = None
    """The blue channel shift in (x, y) directions to correct chromatic aberration."""
    camera_matrix: CameraMatrix | None = None
    """3x3 camera matrix or None."""
    distortion_coefficients: tuple[Point2f, ...] | None = None
    """Sequence of distortion coefficients as Point2f or None."""

    @classmethod
    @field_validator("original_filename", mode="before")
    def _validate_original_filename(cls: type["PhotoData"], v: Any) -> Path | None:  # noqa: ANN401
        if v is None:
            return None
        if isinstance(v, Path):
            return v
        # Coerce strings; raise helpful error for other types
        try:
            s = str(v)
        except Exception as exc:
            msg = "original_filename must be a path-like string or None"
            raise ValueError(msg) from exc
        s = s.strip()
        return Path(s) if s != "" else None

    @classmethod
    @field_validator("quadrat_corners", mode="before")
    def _validate_quadrat_corners(cls: type["PhotoData"], v: Any) -> list[Point2f]:  # noqa: ANN401
        if v is None:
            return []
        try:
            corners = [(float(pt[0]), float(pt[1])) for pt in v]
        except Exception as exc:
            msg = "quadrat_corners must be an iterable of up to 4 [x,y] pairs or None"
            raise ValueError(msg) from exc
        if len(corners) >= 4:
            msg = "quadrat_corners must contain up to 4 points"
            raise ValueError(msg)
        return corners

    @classmethod
    @field_validator("red_shift", mode="before")
    def _validate_red_shift(cls: type["PhotoData"], v: Any) -> tuple[float, float] | None:  # noqa: ANN401
        if v is None:
            return None
        try:
            return float(v[0]), float(v[1])
        except Exception as exc:
            msg = "red_shift must be a pair of numbers or None"
            raise ValueError(msg) from exc

    @classmethod
    @field_validator("blue_shift", mode="before")
    def _validate_blue_shift(cls: type["PhotoData"], v: Any) -> tuple[float, float] | None:  # noqa: ANN401
        if v is None:
            return None
        try:
            return float(v[0]), float(v[1])
        except Exception as exc:
            msg = "blue_shift must be a pair of numbers or None"
            raise ValueError(msg) from exc

    @classmethod
    @field_validator("camera_matrix", mode="before")
    def _validate_camera_matrix(cls: type["PhotoData"], v: Any) -> CameraMatrix | None:  # noqa: ANN401
        if v is None:
            return None
        try:
            rows = [tuple(float(x) for x in row) for row in v]
        except Exception as exc:
            msg = "camera_matrix must be a 3x3 numeric structure or None"
            raise ValueError(msg) from exc
        if len(rows) != 3 or any(len(r) != 3 for r in rows):
            msg = "camera_matrix must be a 3x3 numeric structure"
            raise ValueError(msg)
        return cast(CameraMatrix, (rows[0], rows[1], rows[2]))

    @classmethod
    @field_validator("distortion_coefficients", mode="before")
    def _validate_distortion(cls: type["PhotoData"], v: Any) -> tuple[Point2f, ...] | None:  # noqa: ANN401
        if v is None:
            return None
        try:
            pts = tuple((float(p[0]), float(p[1])) for p in v)
        except Exception as exc:
            msg = "distortion_coefficients must be a sequence of [x,y] pairs or None"
            raise ValueError(msg) from exc
        return pts


class PhotoModel(QModel[PhotoData]):

    on_original_filename_changed: Signal = Signal()
    on_quadrat_corners_changed: Signal = Signal()
    on_red_shift_changed: Signal = Signal()
    on_blue_shift_changed: Signal = Signal()
    on_camera_matrix_changed: Signal = Signal()
    on_distortion_coefficients_changed: Signal = Signal()

    def __init__(self, data: PhotoData | dict[str, Any] | None = None) -> None:
        super().__init__(model_cls=PhotoData, data=data)


    @property
    def original_filename(self) -> Path | None:
        """The original filename of the photo."""
        return self._data.original_filename

    @original_filename.setter
    def original_filename(self, value: str) -> None:
        self._set_field("original_filename", value)

    @property
    def quadrat_corners(self) -> list[Point2f] | None:
        """The corners of the quadrat in the photo, if set."""
        return self._data.quadrat_corners

    @quadrat_corners.setter
    def quadrat_corners(self, value: list[Point2f] | None) -> None:
        self._set_field("quadrat_corners", value)

    @property
    def red_shift(self) -> tuple[float, float] | None:
        """The red channel shift in (x, y) directions to correct chromatic aberration."""
        return self._data.red_shift

    @red_shift.setter
    def red_shift(self, value: tuple[float, float] | None) -> None:
        self._set_field("red_shift", value)

    @property
    def blue_shift(self) -> tuple[float, float] | None:
        """The blue channel shift in (x, y) directions to correct chromatic aberration."""
        return self._data.blue_shift

    @blue_shift.setter
    def blue_shift(self, value: tuple[float, float] | None) -> None:
        self._set_field("blue_shift", value)

    @property
    def camera_matrix(self) -> CameraMatrix | None:
        """3x3 camera matrix or None."""
        return self._data.camera_matrix

    @camera_matrix.setter
    def camera_matrix(self, value: CameraMatrix | None) -> None:
        self._set_field("camera_matrix", value)

    @property
    def distortion_coefficients(self) -> tuple[Point2f, ...] | None:
        """Sequence of distortion coefficients as Point2f or None."""
        return self._data.distortion_coefficients

    @distortion_coefficients.setter
    def distortion_coefficients(self, value: tuple[Point2f, ...] | None) -> None:
        self._set_field("distortion_coefficients", value)
