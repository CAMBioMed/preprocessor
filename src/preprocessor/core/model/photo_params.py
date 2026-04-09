from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from preprocessor.core.model import MetadataData
from preprocessor.core.type_corners import Corners
from preprocessor.core.types import LensVector, CameraMatrix
from preprocessor.model.project_path import ProjectPath


class ColorCorrectionParams(BaseModel, validate_assignment=True):
    """Parameters for color correction."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    # TODO: To be replaced
    gain_r: float = 1.0
    gain_g: float = 1.0
    gain_b: float = 1.0

    # TODO: Implement validation


class LensCorrectionParams(BaseModel, validate_assignment=True):
    """Parameters for lens correction."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    camera_matrix: CameraMatrix | None
    """The 3x3 camera intrinsic matrix, or None to use the default
    (focal lengths = image width, principal point = image center)."""

    coefficients: Annotated[LensVector | None, Field(min_length=4, max_length=14)]
    """Tuple of 4, 5, 8, 12, or 14 distortion coefficients, or None to use all-zero coefficients."""

    @field_validator("coefficients")
    @classmethod
    def _validate_len(cls, v: LensVector) -> LensVector:
        if len(v) not in (4, 5, 8, 12, 14):
            msg = "Lens distortion coefficients must have length 4, 5, 8, 12, or 14"
            raise ValueError(msg)
        if any((x != x) for x in v):  # NaN check without numpy
            msg = "Lens distortion coefficients must not contain NaN"
            raise ValueError(msg)
        return v


class CropParams(BaseModel, validate_assignment=True):
    """Parameters for cropping the photo."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    corners: Corners = Corners(())
    """The (x, y) coordinates of up to 4 corners of the crop rectangle.

    When not Corners.is_valid(), the corners are ignored and no cropping is performed."""


class PhotoData(BaseModel, validate_assignment=True):
    """Parameters for photo processing."""

    model_config = ConfigDict(extra="forbid")

    #######################
    ## Schema properties ##
    #######################

    schema_version: int = Field(1, ge=1)
    """The schema version."""

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

    color_correction: ColorCorrectionParams | None
    """The parameters for color correction, or None to not perform color correction."""
    lens_correction: LensCorrectionParams | None
    """The parameters for lens correction, or None to not perform lens correction."""
    crop: CropParams | None
    """The parameters for cropping the photo, or None to not crop the photo."""

    ##############
    ## Metadata ##
    ##############

    metadata: MetadataData = MetadataData()
    """The metadata for the photo."""

