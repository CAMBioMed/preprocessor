import contextlib
from pathlib import Path
from typing import Any

from PySide6.QtCore import Signal
from pydantic import BaseModel, field_validator, Field

from preprocessor.model import Point2, Matrix3x3
from preprocessor.model.metadata_model import MetadataData, MetadataModel
from preprocessor.model.qmodel import QModel
from preprocessor.utils import update_basepath


class PhotoData(BaseModel):
    """The data for a single photo in the project, used for serialization."""

    ######################
    ## Fixed properties ##
    ######################

    original_filename: Path
    """The path to the photo file, relative to the project."""
    width: int
    """The width of the photo in pixels."""
    height: int
    """The height of the photo in pixels."""

    ######################
    ## Photo correction ##
    ######################

    quadrat_corners: list[Point2] | None = None
    """The up to 4 corners of the quadrat in the photo, or None if not set."""
    camera_matrix: Matrix3x3 | None = None
    """3x3 camera matrix, or None if not set."""
    distortion_coefficients: list[float] | None = None
    """Tuple of 4, 5, 8, 12, or 14 distortion coefficients, or None if not set."""
    red_shift: Point2 | None = None
    """The red channel shift in (x, y) directions to correct chromatic aberration."""
    blue_shift: Point2 | None = None
    """The blue channel shift in (x, y) directions to correct chromatic aberration."""

    ##############
    ## Metadata ##
    ##############

    metadata: MetadataData = MetadataData()
    """The metadata for the photo."""

    @field_validator("quadrat_corners", mode="after")
    @classmethod
    def _validate_quadrat_corners(cls: type["PhotoData"], v: list[Point2] | None) -> list[Point2] | None:
        if v is not None and len(v) > 4:
            msg = "quadrat_corners must be a list of up to 4 Point2 tuples"
            raise ValueError(msg)
        if v is not None and len(v) == 0:
            return None
        return v

    @field_validator("distortion_coefficients", mode="after")
    @classmethod
    def _validate_distortion_coefficients(cls: type["PhotoData"], v: list[float] | None) -> list[float] | None:
        # Accept None (not provided) as valid
        if v is None:
            return None
        if len(v) not in (4, 5, 8, 12, 14):
            msg = "distortion_coefficients must be a tuple of 4, 5, 8, 12, or 14 floats"
            raise ValueError(msg)
        return v


class PhotoModel(QModel[PhotoData]):

    ## Fixed properties
    on_original_filename_changed: Signal = Signal(Path)
    on_width_changed: Signal = Signal(int)
    on_height_changed: Signal = Signal(int)

    ## Photo correction
    on_quadrat_corners_changed: Signal = Signal(object)
    on_red_shift_changed: Signal = Signal(object)
    on_blue_shift_changed: Signal = Signal(object)
    on_camera_matrix_changed: Signal = Signal(object)
    on_distortion_coefficients_changed: Signal = Signal(object)

    ## Metadata
    on_metadata_changed: Signal = Signal()

    _metadata: MetadataModel

    def __init__(self, data: PhotoData | dict[str, Any] | None = None) -> None:
        super().__init__(model_cls=PhotoData, data=data)

        self._metadata = MetadataModel(data=self._data.metadata)
        self._metadata.on_changed.connect(self._handle_metadata_changed)

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

    #############
    ## Helpers ##
    #############

    @property
    def name(self) -> str:
        """The filename of the photo, derived from the original path."""
        return self.original_filename.name

    ######################
    ## Fixed properties ##
    ######################

    @property
    def original_filename(self) -> Path:
        """The original filename of the photo."""
        return self._data.original_filename

    @original_filename.setter
    def original_filename(self, value: Path) -> None:
        self._set_field("original_filename", value)

    @property
    def width(self) -> int:
        """The width of the photo in pixels."""
        return self._data.width

    @width.setter
    def width(self, value: int) -> None:
        self._set_field("width", value)

    @property
    def height(self) -> int:
        """The height of the photo in pixels."""
        return self._data.height

    @height.setter
    def height(self, value: int) -> None:
        self._set_field("height", value)

    ######################
    ## Photo correction ##
    ######################

    @property
    def quadrat_corners(self) -> list[Point2] | None:
        """The corners of the quadrat in the photo, if set."""
        return self._data.quadrat_corners

    @quadrat_corners.setter
    def quadrat_corners(self, value: list[Point2] | None) -> None:
        self._set_field("quadrat_corners", value)

    @property
    def camera_matrix(self) -> Matrix3x3 | None:
        """3x3 camera matrix or None."""
        return self._data.camera_matrix

    @camera_matrix.setter
    def camera_matrix(self, value: Matrix3x3 | None) -> None:
        self._set_field("camera_matrix", value)

    @property
    def distortion_coefficients(self) -> list[float] | None:
        """Sequence of distortion coefficients as Point2 or None."""
        return self._data.distortion_coefficients

    @distortion_coefficients.setter
    def distortion_coefficients(self, value: list[float] | None) -> None:
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

    ##############
    ## Metadata ##
    ##############

    @property
    def metadata(self) -> MetadataModel:
        """The metadata for the photo."""
        return self._metadata

    def _handle_metadata_changed(self) -> None:
        """Handle a change in the metadata."""
        self.mark_dirty()
        with contextlib.suppress(Exception):
            self.on_metadata_changed.emit()
        with contextlib.suppress(Exception):
            self.on_changed.emit()

    def update_paths_relative_to(self, old_basepath: Path, new_basepath: Path) -> None:
        self.original_filename = update_basepath(old_basepath, new_basepath, self.original_filename)
