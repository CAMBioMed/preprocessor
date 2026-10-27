from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from preprocessor.core.serialization.types import LensVector, Matrix3x3


class LensCorrectionParams(BaseModel, validate_assignment=True):
    """Parameters for lens correction."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    enabled: bool = False
    """Whether to perform lens correction. If False, the other parameters are ignored."""

    camera_matrix: Matrix3x3 | None = None
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
        return v
