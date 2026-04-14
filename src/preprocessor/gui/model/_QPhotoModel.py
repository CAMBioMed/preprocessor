from pathlib import Path
from typing import Any

from PySide6.QtCore import Signal

from preprocessor.core.model import PhotoData, MetadataData, ColorCorrectionParams, LensCorrectionParams, CropParams
from preprocessor.gui.model import QModel


class QPhotoModel(QModel[PhotoData]):
    """The model for a single photo in the project, used for the GUI."""

    on_image_id_changed: Signal = Signal(str)
    on_image_path_changed: Signal = Signal(Path)
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
    def image_path(self) -> Path:
        """The path to the photo file, as an absolute path."""
        return self._data.image_path

    @image_path.setter
    def image_path(self, value: Path) -> None:
        self._set_field("image_path", value)

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
        return self.image_path.name
