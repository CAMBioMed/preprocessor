from pydantic import BaseModel, ConfigDict

from preprocessor.core.type_corners import Corners


class CropParams(BaseModel, validate_assignment=True):
    """Parameters for cropping the photo."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    corners: Corners = Corners(())
    """The (x, y) coordinates of up to 4 corners of the crop rectangle.

    When not Corners.is_valid(), the corners are ignored and no cropping is performed."""
