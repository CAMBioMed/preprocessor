from pathlib import Path
from typing import Any, cast, ClassVar

from PySide6.QtCore import Signal
from cv2.typing import Point2f
from pydantic import BaseModel, field_validator, Field

from preprocessor.model.qmodel import QModel

CameraMatrix = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float]
]

class CameraData(BaseModel):
    """The data for a camera, used for serialization."""

    # Serialization JSON version
    SERIAL_VERSION: ClassVar[int] = 1

    file: Path | None = Field(default=None, exclude=True)
    """The file path of the camera calibration file, or None if not set. This is not serialized/deserialized."""
    name: str = ""
    """The name of the camera."""
    camera_matrix: CameraMatrix | None = None
    """A 3x3 camera matrix as a tuple of 3 tuples; or None if not set."""
    distortion_coefficients: tuple[Point2f, ...] | None = None
    """A sequence of distortion coefficients; or None if not set."""

    @classmethod
    @field_validator("file", mode="before")
    def _validate_file(cls: type["CameraData"], v: Any) -> Path | None:  # noqa: ANN401
        if v is None:
            return None
        if isinstance(v, Path):
            return v
        # Coerce strings; raise helpful error for other types
        try:
            s = str(v)
        except Exception as exc:
            msg = "file must be a path-like string or None"
            raise ValueError(msg) from exc
        s = s.strip()
        return Path(s) if s != "" else None

    @classmethod
    @field_validator("camera_matrix", mode="before")
    def _validate_camera_matrix(cls: type["CameraData"], v: Any) -> CameraMatrix | None:  # noqa: ANN401
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
    def _validate_distortion(cls: type["CameraData"], v: Any) -> tuple[Point2f, ...] | None:  # noqa: ANN401
        if v is None:
            return None
        try:
            pts = tuple((float(p[0]), float(p[1])) for p in v)
        except Exception as exc:
            msg = "distortion_coefficients must be a sequence of [x,y] pairs or None"
            raise ValueError(msg) from exc
        return pts


class CameraModel(QModel[CameraData]):

    on_file_changed: Signal = Signal(object)
    on_name_changed: Signal = Signal(str)
    on_camera_matrix_changed: Signal = Signal()
    on_distortion_coefficients_changed: Signal = Signal()

    def __init__(self, data: CameraData | dict[str, Any] | None = None) -> None:
        super().__init__(model_cls=CameraData, data=data)

    @property
    def file(self) -> Path | None:
        """
        The file path of the camera calibration file, or None if not set.

        This property is not serialized/deserialized.
        """
        return self._data.file

    @file.setter
    def file(self, value: Path | None) -> None:
        self._set_field("file", value)

    @property
    def name(self) -> str:
        """The name of the camera."""
        return self._data.name

    @name.setter
    def name(self, value: str) -> None:
        self._set_field("name", value)

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
