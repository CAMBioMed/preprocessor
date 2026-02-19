from pathlib import Path
from typing import Any, cast

from PySide6.QtCore import Signal
from pydantic import BaseModel, field_validator, ValidationError

from preprocessor.model import Point2
from preprocessor.model.camera_model import CameraMatrix
from preprocessor.model.qmodel import QModel


class PhotoData(BaseModel):
    """The data for a single photo in the project, used for serialization."""

    original_filename: Path | None = None
    """The original path to the photo file, if set."""
    quadrat_corners: list[Point2] = []
    """The corners of the quadrat in the photo, if set."""
    red_shift: Point2 | None = None
    """The red channel shift in (x, y) directions to correct chromatic aberration."""
    blue_shift: Point2 | None = None
    """The blue channel shift in (x, y) directions to correct chromatic aberration."""
    camera_matrix: CameraMatrix | None = None
    """3x3 camera matrix or None."""
    distortion_coefficients: tuple[Point2, ...] | None = None
    """Sequence of distortion coefficients as Point2 or None."""

    @field_validator("quadrat_corners", mode="after")
    @classmethod
    def _validate_quadrat_corners(cls: type["PhotoData"], v: list[Point2]) -> list[Point2]:
        if v is None:
            return []
        try:
            corners = [(float(pt[0]), float(pt[1])) for pt in v]
        except Exception as exc:
            msg = "quadrat_corners must be an iterable of up to 4 [x,y] pairs or None"
            raise ValueError(msg) from exc
        if len(corners) > 4:
            msg = "quadrat_corners must contain up to 4 points"
            raise ValueError(msg)
        return corners

    @field_validator("camera_matrix", mode="after")
    @classmethod
    def _validate_camera_matrix(cls: type["PhotoData"], v: CameraMatrix | None) -> CameraMatrix | None:
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
    def original_filename(self, value: Path | None) -> None:
        self._set_field("original_filename", value)

    @property
    def quadrat_corners(self) -> list[Point2] | None:
        """The corners of the quadrat in the photo, if set."""
        return self._data.quadrat_corners

    @quadrat_corners.setter
    def quadrat_corners(self, value: list[Point2] | None) -> None:
        self._set_field("quadrat_corners", value)

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

    @property
    def camera_matrix(self) -> CameraMatrix | None:
        """3x3 camera matrix or None."""
        return self._data.camera_matrix

    @camera_matrix.setter
    def camera_matrix(self, value: CameraMatrix | None) -> None:
        self._set_field("camera_matrix", value)

    @property
    def distortion_coefficients(self) -> tuple[Point2, ...] | None:
        """Sequence of distortion coefficients as Point2 or None."""
        return self._data.distortion_coefficients

    @distortion_coefficients.setter
    def distortion_coefficients(self, value: tuple[Point2, ...] | None) -> None:
        self._set_field("distortion_coefficients", value)

    def write_to_file(self, path: str | Path) -> None:
        """
        Write the serialized project JSON to the given file path.
        Parent directories will be created if necessary.
        """
        p = Path(path)
        if p.parent:
            p.parent.mkdir(parents=True, exist_ok=True)
        json_str = self.write_to_json()
        with p.open("w", encoding="utf-8") as fh:
            fh.write(json_str)
        self.file = Path(path)
        self.mark_clean()

    def write_to_json(self) -> str:
        """Return a JSON string representation of the model."""
        return self._data.model_dump_json()

    @classmethod
    def read_from_file(cls: type["PhotoModel"], path: str | Path) -> "PhotoModel":
        """
        Load project JSON from the given file path and apply via deserialize().
        Raises FileNotFoundError if the path does not exist.
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(str(p))
        with p.open("r", encoding="utf-8") as fh:
            json_str = fh.read()
        return cls.read_from_json(json_str)

    @classmethod
    def read_from_json(cls: type["PhotoModel"], json_str: str) -> "PhotoModel":
        """Load model data from a JSON string."""
        try:
            new_data = PhotoData.model_validate_json(json_str)  # type: ignore[arg-type]
        except ValidationError as exc:
            raise ValueError(str(exc)) from exc

        return PhotoModel(data=new_data)
