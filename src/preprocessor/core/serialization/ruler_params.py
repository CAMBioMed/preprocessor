from pydantic import BaseModel, ConfigDict, Field

from preprocessor.core.serialization.point2d import Point2D


class RulerParams(BaseModel, validate_assignment=True):
    """Parameters for displaying a ruler."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    enabled: bool = False
    """Whether to display the ruler. If False, the other parameters are ignored."""

    points: tuple[Point2D, ...] = Field(
        description=(
            "The (x, y) coordinates of up to 2 corners of the ruler, "
            "as image-pixel (x, y) coordinates measured from the top-left origin, "
            "with x increasing rightward and y increasing downward."
        ),
        max_length=2,
        default_factory=tuple,
    )
