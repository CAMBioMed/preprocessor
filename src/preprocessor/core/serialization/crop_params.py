import math
from collections.abc import Sequence

from pydantic import BaseModel, ConfigDict, Field

from preprocessor.core.serialization import Point2D


class CropParams(BaseModel, validate_assignment=True):
    """Parameters for cropping the photo."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    enabled: bool = False
    """Whether to perform cropping. If False, the other parameters are ignored."""

    quadrat: tuple[Point2D, ...] = Field(
        description=(
            "The (x, y) coordinates of up to 4 corners of the crop rectangle, "
            "as image-pixel (x, y) coordinates measured from the top-left origin, "
            "with x increasing rightward and y increasing downward."
        ),
        max_length=4,
        default_factory=tuple,
    )

    def quadrat_clockwise(self) -> tuple[Point2D, Point2D, Point2D, Point2D]:
        """Return the corners ordered in a consistent polygon traversal order.

        The returned order is clockwise from the top-left, lowest y first.

        Call is_valid() first to check if the corners are valid (i.e., 4 corners and non-degenerate)
        before calling this method.

        :return: A tuple of 4 points ordered as (top-left, top-right, bottom-right, bottom-left).
        :raises ValueError: If the corners are not valid (e.g., not 4 corners or degenerate).
        """
        return _clockwise_corners(self.quadrat)

    @property
    def quadrat_tl(self) -> Point2D:
        """The top-left corner of the quadrilateral, as a (x, y) tuple.

        :return: The top-left corner of the quadrilateral.
        :raises ValueError: If the corners are not valid (e.g., not 4 corners or degenerate).
        """
        return self.quadrat_clockwise()[0]

    @property
    def quadrat_tr(self) -> Point2D:
        """The top-right corner of the quadrilateral, as a (x, y) tuple.

        :return: The top-right corner of the quadrilateral.
        :raises ValueError: If the corners are not valid (e.g., not 4 corners or degenerate).
        """
        return self.quadrat_clockwise()[1]

    @property
    def quadrat_br(self) -> Point2D:
        """The bottom-right corner of the quadrilateral, as a (x, y) tuple.

        :return: The bottom-right corner of the quadrilateral.
        :raises ValueError: If the corners are not valid (e.g., not 4 corners or degenerate).
        """
        return self.quadrat_clockwise()[2]

    @property
    def quadrat_bl(self) -> Point2D:
        """The bottom-left corner of the quadrilateral, as a (x, y) tuple.

        :return: The bottom-left corner of the quadrilateral.
        :raises ValueError: If the corners are not valid (e.g., not 4 corners or degenerate).
        """
        return self.quadrat_clockwise()[3]

    def quadrat_as_tuple(self) -> tuple[Point2D, ...]:
        """Return the corners as a tuple of (x, y) points.

        If the corners are valid (4 corners and non-degenerate), they will be returned in a consistent polygon
        traversal order (top-left, top-right, bottom-right, bottom-left).

        :return: A tuple of (x, y) points representing the corners.
        """
        try:
            return self.quadrat_clockwise()
        except ValueError:
            return self.quadrat


def _clockwise_corners(points: Sequence[Point2D]) -> tuple[Point2D, Point2D, Point2D, Point2D]:
    """Helper function to return the points ordered in a consistent polygon traversal order.

    The returned order is clockwise from the top-left, lowest y first.

    Call is_valid() first to check if the corners are valid (i.e., 4 corners and non-degenerate)
    before calling this method.

    :return: A tuple of 4 points ordered as (top-left, top-right, bottom-right, bottom-left).
    :raises ValueError: If the corners are not valid (e.g., not 4 corners or degenerate).
    """
    if len(points) != 4:
        msg = "Expected exactly 4 points"
        raise ValueError(msg)

    if len(set(points)) != 4:
        msg = "Expected 4 distinct points"
        raise ValueError(msg)

    # Calculate centroid.
    cx = sum(x for x, y in points) / 4
    cy = sum(y for x, y in points) / 4

    # Sort by angle around centroid. In image coordinates (+y downward), this corresponds to a clockwise traversal.
    clockwise = sorted(
        points,
        key=lambda p: math.atan2(p[1] - cy, p[0] - cx),
    )

    # Verify strict convexity using consecutive cross products.
    for i in range(4):
        ax, ay = clockwise[i]
        bx, by = clockwise[(i + 1) % 4]
        dx, dy = clockwise[(i + 2) % 4]

        cross = (bx - ax) * (dy - by) - (by - ay) * (dx - bx)

        if cross <= 0:
            msg = "Quadrilateral must be strictly convex"
            raise ValueError(msg)

    # Rotate sequence to start with the topmost vertex.
    start = min(range(4), key=lambda i: (clockwise[i][1], clockwise[i][0]))
    clockwise = clockwise[start:] + clockwise[:start]

    # Ensure non-degenerate quad (area != 0)
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = clockwise
    area = abs(x1 * y2 - y1 * x2 + x2 * y3 - y2 * x3 + x3 * y4 - y3 * x4 + x4 * y1 - y4 * x1)
    if area == 0:
        msg = "Degenerate quad (area is zero)"
        raise ValueError(msg)

    return (clockwise[0], clockwise[1], clockwise[2], clockwise[3])
