import math
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from preprocessor.core.types import CameraMatrix, LensVector


class LensCorrectionParams(BaseModel, validate_assignment=True):
    """Parameters for correcting lens distortion in a photo."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    enabled: bool = False
    """Whether to perform lens correction. If False, the other parameters are ignored."""

    camera_matrix: CameraMatrix | None = None
    """The 3x3 camera intrinsic matrix, or None to use the default."""

    coefficients: Annotated[LensVector | None, Field(min_length=4, max_length=14)] = None
    """The distortion coefficients, or None to use all-zero coefficients."""

    @field_validator("coefficients", mode="after")
    @classmethod
    def validate_coefficients(cls, value: LensVector | None) -> LensVector | None:
        """Validate the supported distortion-coefficient lengths and values."""
        if value is None:
            return None
        if len(value) not in (4, 5, 8, 12, 14):
            msg = "Lens distortion coefficients must have length 4, 5, 8, 12, or 14"
            raise ValueError(msg)
        if any(not math.isfinite(coefficient) for coefficient in value):
            msg = "Lens distortion coefficients must be finite"
            raise ValueError(msg)
        return value

    @field_validator("camera_matrix", mode="after")
    @classmethod
    def validate_camera_matrix(cls, value: CameraMatrix | None) -> CameraMatrix | None:
        """Validate the camera matrix dimensions and values."""
        if value is None:
            return None
        if len(value) != 3 or any(len(row) != 3 for row in value):
            msg = "Camera matrix must be 3x3"
            raise ValueError(msg)
        if any(not math.isfinite(coordinate) for row in value for coordinate in row):
            msg = "Camera matrix values must be finite"
            raise ValueError(msg)
        return value
