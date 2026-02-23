from pathlib import Path
from typing import Any

from PySide6.QtCore import Signal
from pydantic import BaseModel, field_validator, Field

from preprocessor.model import Point2, Matrix3x3
from preprocessor.model.qmodel import QModel
from preprocessor.utils import update_basepath


class PhotoData(BaseModel):
    """The data for a single photo in the project, used for serialization."""

    original_filename: Path
    """The path to the photo file, relative to the project."""
    width: int
    """The width of the photo in pixels."""
    height: int
    """The height of the photo in pixels."""
    quadrat_corners: list[Point2] = []
    """The up to 4 corners of the quadrat in the photo."""
    camera_matrix: Matrix3x3 = Field(
        default_factory=lambda d: (
            (float(d["width"]), 0, float(d["width"]) / 2),
            (0, float(d["width"]), float(d["height"]) / 2),
            (0, 0, 1),
        )
    )
    """3x3 camera matrix or None."""
    distortion_coefficients: list[float] = [0, 0, 0, 0, 0]
    """Tuple of 4, 5, 8, 12, or 14 distortion coefficients."""
    red_shift: Point2 | None = None
    """The red channel shift in (x, y) directions to correct chromatic aberration."""
    blue_shift: Point2 | None = None
    """The blue channel shift in (x, y) directions to correct chromatic aberration."""

    @field_validator("distortion_coefficients", mode="after")
    @classmethod
    def _validate_distortion_coefficients(cls: type["PhotoData"], v: list[float]) -> list[float]:
        if len(v) not in (4, 5, 8, 12, 14):
            msg = "distortion_coefficients must be a tuple of 4, 5, 8, 12, or 14 floats"
            raise ValueError(msg)
        return v


class PhotoModel(QModel[PhotoData]):
    on_original_filename_changed: Signal = Signal()
    on_quadrat_corners_changed: Signal = Signal()
    on_red_shift_changed: Signal = Signal()
    on_blue_shift_changed: Signal = Signal()
    on_camera_matrix_changed: Signal = Signal()
    on_distortion_coefficients_changed: Signal = Signal()

    def __init__(self, data: PhotoData | dict[str, Any] | None = None) -> None:
        super().__init__(model_cls=PhotoData, data=data)

    @classmethod
    def from_file(cls, fullpath: Path, basepath: Path | None) -> "PhotoModel":
        """Create a PhotoModel from a photo file, extracting its dimensions."""
        from PIL import Image

        relative_path = update_basepath(None, basepath, fullpath)
        with Image.open(fullpath) as img:
            width, height = img.size

        data = PhotoData(
            original_filename=relative_path,
            width=width,
            height=height,
        )
        return cls(data=data)

    @property
    def original_filename(self) -> Path:
        """The original filename of the photo."""
        return self._data.original_filename

    @original_filename.setter
    def original_filename(self, value: Path) -> None:
        self._set_field("original_filename", value)

    @property
    def name(self) -> str:
        """The filename of the photo, derived from the original path."""
        return self.original_filename.name

    @property
    def quadrat_corners(self) -> list[Point2] | None:
        """The corners of the quadrat in the photo, if set."""
        return self._data.quadrat_corners

    @quadrat_corners.setter
    def quadrat_corners(self, value: list[Point2] | None) -> None:
        self._set_field("quadrat_corners", value)

    @property
    def camera_matrix(self) -> Matrix3x3:
        """3x3 camera matrix or None."""
        return self._data.camera_matrix

    @camera_matrix.setter
    def camera_matrix(self, value: Matrix3x3) -> None:
        self._set_field("camera_matrix", value)

    @property
    def distortion_coefficients(self) -> list[float]:
        """Sequence of distortion coefficients as Point2 or None."""
        return self._data.distortion_coefficients

    @distortion_coefficients.setter
    def distortion_coefficients(self, value: list[float]) -> None:
        self._set_field("distortion_coefficients", value)

    @property
    def red_shift(self) -> Point2 | None:
        """The red channel shift in (x, y) directions to correct chromatic aberration."""
        return self._data.red_shift

    @red_shift.setter
    def red_shift(self, value: Point2 | None) -> None:
        self._set_field("red_shift", value)

    @property
    def blue_shift(self) -> Point2 | None:
        """The blue channel shift in (x, y) directions to correct chromatic aberration."""
        return self._data.blue_shift

    @blue_shift.setter
    def blue_shift(self, value: Point2 | None) -> None:
        self._set_field("blue_shift", value)

    def update_paths_relative_to(self, old_basepath: Path, new_basepath: Path) -> None:
        self.original_filename = update_basepath(old_basepath, new_basepath, self.original_filename)
