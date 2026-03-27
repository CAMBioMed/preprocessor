from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from preprocessor.core.types import Corners, LensVector


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

    coefficients: Annotated[LensVector, Field(min_length=4, max_length=14)]
    """Tuple of 4, 5, 8, 12, or 14 distortion coefficients."""

    @field_validator("coefficients")
    @classmethod
    def _validate_len(cls, v: LensVector) -> LensVector:
        if len(v) not in (4, 5, 8, 12, 14):
            raise ValueError("Lens distortion coefficients must have length 4, 5, 8, 12, or 14")
        if any((x != x) for x in v):  # NaN check without numpy
            raise ValueError("Lens distortion coefficients must not contain NaN")
        return v

class CropParams(BaseModel, validate_assignment=True):
    """Parameters for cropping the photo."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    corners: Corners = Corners(())
    """The (x, y) coordinates of up to 4 corners of the crop rectangle.
    
    When not Corners.is_valid(), the corners are ignored and no cropping is performed."""

class PhotoParams(BaseModel, validate_assignment=True):
    """Parameters for photo processing."""

    model_config = ConfigDict(extra="forbid")

    # Future-proofing / provenance
    schema_version: int = Field(1, ge=1)
    """The schema version."""

    # Transformation parameters
    color_correction: ColorCorrectionParams | None
    """The parameters for color correction, or None to not perform color correction."""
    lens_correction: LensCorrectionParams | None
    """The parameters for lens correction, or None to not perform lens correction."""
    crop: CropParams | None
    """The parameters for cropping the photo, or None to not crop the photo."""