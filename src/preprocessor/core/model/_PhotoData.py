from pydantic import BaseModel, ConfigDict

from preprocessor.core.model._MetadataData import MetadataData
from preprocessor.core.model._ColorCorrectionParams import ColorCorrectionParams
from preprocessor.core.model._LensCorrectionParams import LensCorrectionParams
from preprocessor.core.model._CropParams import CropParams
from preprocessor.core.model._ProjectPath import ProjectPath




class PhotoData(BaseModel, validate_assignment=True):
    """Parameters for photo processing."""

    model_config = ConfigDict(
        extra="forbid",
    )

    ######################
    ## Fixed properties ##
    ######################

    image_id: str
    """The unique identifier for the photo."""
    image_path: ProjectPath
    """The path to the photo file, relative to the project."""

    ######################
    ## Photo correction ##
    ######################

    color_correction: ColorCorrectionParams | None = None
    """The parameters for color correction, or None to not perform color correction."""
    lens_correction: LensCorrectionParams | None = None
    """The parameters for lens correction, or None to not perform lens correction."""
    crop: CropParams | None = None
    """The parameters for cropping the photo, or None to not crop the photo."""

    ##############
    ## Metadata ##
    ##############

    metadata: MetadataData = MetadataData()
    """The metadata for the photo."""

