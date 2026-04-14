from pathlib import Path
from typing import Any

from PySide6.QtCore import Signal

from preprocessor.core.model import PhotoData, MetadataData, ColorCorrectionParams, LensCorrectionParams, CropParams
from preprocessor.core.type_corners import Corners
from preprocessor.core.types import Point2D, CameraMatrix
from preprocessor.gui.model import QModel


class QPhotoModel(QModel[PhotoData]):
    """The model for a single photo in the project, used for the GUI."""

    on_image_id_changed: Signal = Signal(str)
    on_original_filename_changed: Signal = Signal(Path)
    on_color_correction_changed: Signal = Signal(object)  # Emits ColorCorrectionParams | None
    on_lens_correction_changed: Signal = Signal(object)  # Emits LensCorrectionParams | None
    on_crop_changed: Signal = Signal(object)  # Emits CropParams | None
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
    def color_correction(self) -> ColorCorrectionParams | None:
        """The parameters for color correction, or None to not perform color correction."""
        return self._data.color_correction

    @color_correction.setter
    def color_correction(self, value: ColorCorrectionParams | None) -> None:
        self._set_field("color_correction", value)

    @property
    def lens_correction(self) -> LensCorrectionParams | None:
        """The parameters for lens correction, or None to not perform lens correction."""
        return self._data.lens_correction

    @lens_correction.setter
    def lens_correction(self, value: LensCorrectionParams | None) -> None:
        self._set_field("lens_correction", value)

    @property
    def crop(self) -> CropParams | None:
        """The parameters for cropping the photo, or None to not crop the photo."""
        return self._data.crop

    @crop.setter
    def crop(self, value: CropParams | None) -> None:
        self._set_field("crop", value)

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

    # TODO: Replace by direct submodel access:
    @property
    def quadrat_corners(self) -> list[Point2D] | None:
        """The corners of the quadrat in the photo, if set."""
        if self._data.crop is None:
            return None
        return list(self._data.crop.corners.as_tuple())

    # TODO: Replace by direct submodel access:
    @quadrat_corners.setter
    def quadrat_corners(self, value: list[Point2D] | None) -> None:
        if value is None:
            self.crop = None
        else:
            self.crop = CropParams(corners=Corners(tuple(value)))

    # TODO: Replace by direct submodel access:
    @property
    def camera_matrix(self) -> CameraMatrix | None:
        """3x3 camera matrix or None."""
        if self._data.lens_correction is None:
            return None
        return self._data.lens_correction.camera_matrix

    # TODO: Replace by direct submodel access:
    @camera_matrix.setter
    def camera_matrix(self, value: CameraMatrix | None) -> None:
        old_model = self._data.lens_correction
        new_model = LensCorrectionParams.model_validate({
            **(old_model.model_dump() if old_model is not None else {}),
            "camera_matrix": value,
        })
        self._data.lens_correction = new_model

    # TODO: Replace by direct submodel access:
    @property
    def distortion_coefficients(self) -> list[float] | None:
        """Sequence of distortion coefficients as Point2 or None."""
        if self._data.lens_correction is None:
            return None
        return self._data.lens_correction.coefficients

    # TODO: Replace by direct submodel access:
    @distortion_coefficients.setter
    def distortion_coefficients(self, value: list[float] | None) -> None:
        old_model = self._data.lens_correction
        new_model = LensCorrectionParams.model_validate({
            **(old_model.model_dump() if old_model is not None else {}),
            "coefficients": value,
        })
        self._data.lens_correction = new_model
