from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from preprocessor.core.types import LensVector, CameraMatrix


class LensCorrectionParams(BaseModel, validate_assignment=True):
    """Parameters for lens correction."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    enabled: bool = False
    """Whether to perform lens correction. If False, the other parameters are ignored."""

    camera_matrix: CameraMatrix | None = None
    """The 3x3 camera intrinsic matrix, or None to use the default
    (focal lengths = image width, principal point = image center)."""

    coefficients: Annotated[LensVector | None, Field(min_length=4, max_length=14)] = None
    """Tuple of 4, 5, 8, 12, or 14 distortion coefficients, or None to use all-zero coefficients."""

    @field_validator("coefficients", mode="after")
    @classmethod
    def _validate_len(cls, v: LensVector | None) -> LensVector | None:
        if v is None:
            return None
        if len(v) not in (4, 5, 8, 12, 14):
            msg = "Lens distortion coefficients must have length 4, 5, 8, 12, or 14"
            raise ValueError(msg)
        if any((x != x) for x in v):  # NaN check without numpy
            msg = "Lens distortion coefficients must not contain NaN"
            raise ValueError(msg)
        return v

    @field_validator("camera_matrix", mode="after")
    @classmethod
    def _validate_camera_matrix(cls, v: CameraMatrix | None) -> CameraMatrix | None:
        if v is None:
            return None
        if len(v) != 3 or any(len(row) != 3 for row in v):
            msg = "Camera matrix must be 3x3"
            raise ValueError(msg)
        if any((x != x) for row in v for x in row):  # NaN check without numpy
            msg = "Camera matrix must not contain NaN"
            raise ValueError(msg)
        return v
