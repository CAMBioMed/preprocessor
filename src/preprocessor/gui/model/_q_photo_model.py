from pathlib import Path
from typing import Any

from PySide6.QtCore import Signal

from preprocessor.core.model import MetadataData, PhotoData
from preprocessor.core.serialization import (
    CropParams,
    LensCorrectionParams,
    Matrix3x3,
    Point2D,
    RulerParams,
)
from preprocessor.gui.model._q_model import QModel


class QPhotoModel(QModel[PhotoData]):
    """The model for a single photo in the project, used for the GUI."""

    on_image_id_changed: Signal = Signal(str)
    on_original_filename_changed: Signal = Signal(Path)
    on_lens_correction_changed: Signal = Signal(object)  # Emits LensCorrectionParams | None
    on_crop_changed: Signal = Signal(object)  # Emits CropParams | None
    on_ruler_changed: Signal = Signal(object)  # Emits RulerParams
    on_metadata_changed: Signal = Signal(object)  # Emits MetadataData

    def __init__(self, data: PhotoData | dict[str, Any] | None = None) -> None:
        super().__init__(model_cls=PhotoData, data=data)

    ######################
    ## Fixed properties ##
    ######################

    @property
    def image_id(self) -> str:
        """The unique ID of the photo."""
        return self._data.image_id

    @image_id.setter
    def image_id(self, value: str) -> None:
        self._set_field("image_id", value)

    @property
    def original_filename(self) -> Path:
        """The path to the photo file, as an absolute path."""
        return self._data.original_filename

    @original_filename.setter
    def original_filename(self, value: Path) -> None:
        self._set_field("original_filename", value)

    ######################
    ## Photo correction ##
    ######################

    @property
    def lens_correction(self) -> LensCorrectionParams:
        """The parameters for lens correction."""
        return self._data.lens_correction

    @lens_correction.setter
    def lens_correction(self, value: LensCorrectionParams) -> None:
        self._set_field("lens_correction", value)

    @property
    def crop(self) -> CropParams:
        """The parameters for cropping the photo."""
        return self._data.crop

    @crop.setter
    def crop(self, value: CropParams) -> None:
        self._set_field("crop", value)

    @property
    def ruler(self) -> RulerParams:
        """The parameters for displaying a ruler on the photo."""
        return self._data.ruler

    @ruler.setter
    def ruler(self, value: RulerParams) -> None:
        self._set_field("ruler", value)

    @property
    def ruler_points(self) -> "list[Point2D]":
        """The ruler points in image coordinates (0, 1, or 2 items)."""
        if not self._data.ruler.enabled:
            return []
        return list(self._data.ruler.points)

    @ruler_points.setter
    def ruler_points(self, value: "list[Point2D] | None") -> None:
        self.ruler = RulerParams(enabled=bool(value), points=tuple(value or ()))

    ##############
    ## Metadata ##
    ##############

    @property
    def metadata(self) -> MetadataData:
        """The metadata for the photo."""
        return self._data.metadata

    @metadata.setter
    def metadata(self, value: MetadataData) -> None:
        self._set_field("metadata", value)

    #############
    ## Helpers ##
    #############

    @property
    def name(self) -> str:
        """The name of the photo, derived from the original path."""
        return self.original_filename.name

    @property
    def quadrat_corners(self) -> list[Point2D] | None:
        """The corners of the quadrat in the photo, if set."""
        if not self._data.crop.enabled:
            return None
        return list(self._data.crop.quadrat_as_tuple())

    @quadrat_corners.setter
    def quadrat_corners(self, value: list[Point2D] | None) -> None:
        self.crop = CropParams(
            enabled=value is not None,
            quadrat=tuple(value or ()),
        )

    # TODO: Replace by direct submodel access:
    @property
    def camera_matrix(self) -> Matrix3x3 | None:
        """3x3 camera matrix or None."""
        if not self.lens_correction.enabled:
            return None
        return self.lens_correction.camera_matrix

    # TODO: Replace by direct submodel access:
    @camera_matrix.setter
    def camera_matrix(self, value: Matrix3x3 | None) -> None:
        old_model = self.lens_correction
        new_model = LensCorrectionParams.model_validate(
            {
                **(old_model.model_dump() if old_model is not None else {}),
                "enabled": value is not None,
                "camera_matrix": value,
            }
        )
        self.lens_correction = new_model

    # TODO: Replace by direct submodel access:
    @property
    def distortion_coefficients(self) -> list[float] | None:
        """Sequence of distortion coefficients as Point2 or None."""
        if not self.lens_correction.enabled:
            return None
        return self.lens_correction.coefficients

    # TODO: Replace by direct submodel access:
    @distortion_coefficients.setter
    def distortion_coefficients(self, value: list[float] | None) -> None:
        old_model = self.lens_correction
        new_model = LensCorrectionParams.model_validate(
            {
                **(old_model.model_dump() if old_model is not None else {}),
                "enabled": value is not None,
                "coefficients": value,
            }
        )
        self.lens_correction = new_model
