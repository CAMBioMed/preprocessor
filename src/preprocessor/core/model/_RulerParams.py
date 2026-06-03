from pydantic import BaseModel, ConfigDict

from preprocessor.core.types import Point2D


class RulerParams(BaseModel, validate_assignment=True):
    """Parameters for displaying a ruler."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    enabled: bool = False
    """Whether to display the ruler. If False, the other parameters are ignored."""

    start: Point2D = (0.0, 0.0)
    """The (x, y) coordinates of the start point of the ruler."""
    end: Point2D | None = None
    """The (x, y) coordinates of the end point of the ruler, or None if only the start has been placed."""
