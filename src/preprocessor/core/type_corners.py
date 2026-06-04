from typing import overload, Any
from collections.abc import Sequence, Iterator

from pydantic import RootModel, ConfigDict, field_validator

from preprocessor.core.types import Point2D


class Corners(RootModel[tuple[Point2D, ...]]):
    """A tuple of up to 4 Point2D representing the corners of a quadrilateral.

    Use the is_valid() method to check if the corners are valid (i.e., 4 corners and non-degenerate).
    Use the ordered() method to get the corners in a consistent order (top-left, top-right, bottom-right, bottom-left).
    """

    model_config = ConfigDict(frozen=True)

    @field_validator("root")
    @classmethod
    def _validate_and_normalize(
        cls,
        v: tuple[Point2D, Point2D, Point2D, Point2D],
    ) -> tuple[Point2D, Point2D, Point2D, Point2D]:
        if len(v) > 4:
            msg = "Expected at most 4 corners"
            raise ValueError(msg)

        # Sanity check
        for x, y in v:
            if x != x or y != y:
                msg = "Corner coordinates must not contain NaN"
                raise ValueError(msg)

        # We specifically allow negative coordinates (the user may drag off-canvas),
        # less than 4 coordinates (the user may not have specified all of them yet),
        # or the quad to be degenerate (the user may have dragged corners on top of each other).
        # Use the is_valid() method to check if the corners are valid (i.e., 4 corners and non-degenerate).

        return v

    # BaseModel defines __iter__ with a different signature (to allow access to the fields)
    # We should not override it here.
    def __iter__(self) -> Iterator[Point2D]:  # type: ignore[override, ty:invalid-method-override]
        return iter(self.root)

    def __len__(self) -> int:
        return len(self.root)

    @overload
    def __getitem__(self, i: int) -> Point2D: ...
    @overload
    def __getitem__(self, i: slice) -> tuple[Point2D, ...]: ...

    def __getitem__(self, i: int | slice) -> Any:
        return self.root[i]

    def is_valid(self) -> bool:
        """Check if the corners are valid (i.e., 4 corners and non-degenerate).

        :return: True if the corners are valid; otherwise, False.
        """
        try:
            self.ordered()
            return True
        except ValueError:
            return False

    def ordered(self) -> tuple[Point2D, Point2D, Point2D, Point2D]:
        """Return the corners ordered in a consistent polygon traversal order.

        The returned order is (top-left, top-right, bottom-right, bottom-left).

        Call is_valid() first to check if the corners are valid (i.e., 4 corners and non-degenerate)
        before calling this method.

        :return: A tuple of 4 points ordered as (top-left, top-right, bottom-right, bottom-left).
        :raises ValueError: If the corners are not valid (e.g., not 4 corners or degenerate).
        """
        # Needs to have exactly 4 corners
        if len(self.root) != 4:
            msg = "Expected exactly 4 corners"
            raise ValueError(msg)

        # Coordinates must be non-negative and within image bounds (can't have corners off the canvas)
        for x, y in self.root:
            if x < 0 or y < 0:
                msg = "Corner coordinates must be non-negative"
                raise ValueError(msg)

        # Try to order the corners
        ordered = _order_corners(self.root)

        # Ensure non-degenerate quad (area != 0)
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = ordered
        area = abs(x1 * y2 - y1 * x2 + x2 * y3 - y2 * x3 + x3 * y4 - y3 * x4 + x4 * y1 - y4 * x1)
        if area == 0:
            msg = "Degenerate quad (area is zero)"
            raise ValueError(msg)

        return ordered

    @property
    def tl(self) -> Point2D:
        """The top-left corner of the quadrilateral, as a (x, y) tuple.

        :return: The top-left corner of the quadrilateral.
        :raises ValueError: If the corners are not valid (e.g., not 4 corners or degenerate).
        """
        return self.ordered()[0]

    @property
    def tr(self) -> Point2D:
        """The top-right corner of the quadrilateral, as a (x, y) tuple.

        :return: The top-right corner of the quadrilateral.
        :raises ValueError: If the corners are not valid (e.g., not 4 corners or degenerate).
        """
        return self.ordered()[1]

    @property
    def bl(self) -> Point2D:
        """The bottom-left corner of the quadrilateral, as a (x, y) tuple.

        :return: The bottom-left corner of the quadrilateral.
        :raises ValueError: If the corners are not valid (e.g., not 4 corners or degenerate).
        """
        return self.ordered()[3]

    @property
    def br(self) -> Point2D:
        """The bottom-right corner of the quadrilateral, as a (x, y) tuple.

        :return: The bottom-right corner of the quadrilateral.
        :raises ValueError: If the corners are not valid (e.g., not 4 corners or degenerate).
        """
        return self.ordered()[2]

    def as_tuple(self) -> tuple[Point2D, ...]:
        """Return the corners as a tuple of (x, y) points.

        If the corners are valid (4 corners and non-degenerate), they will be returned in a consistent polygon
        traversal order (top-left, top-right, bottom-right, bottom-left).

        :return: A tuple of (x, y) points representing the corners.
        """
        try:
            return self.ordered()
        except ValueError:
            return self.root


def _order_corners(points: Sequence[Point2D]) -> tuple[Point2D, Point2D, Point2D, Point2D]:
    """Helper function to order 4 points in polygon traversal order: top-left, top-right, bottom-right, bottom-left.

    :param points: A sequence of 4 (x, y) points.
    :return: A tuple of 4 points ordered as (top-left, top-right, bottom-right, bottom-left).
    :raises ValueError: If the input does not contain exactly 4 points,
    or if the corners are ambiguous (e.g., duplicate points).
    """
    if len(points) != 4:
        msg = "Expected 4 points"
        raise ValueError(msg)

    pts = list(points)
    s = [p[0] + p[1] for p in pts]
    d = [p[0] - p[1] for p in pts]

    tl = pts[int(min(range(4), key=lambda i: s[i]))]
    br = pts[int(max(range(4), key=lambda i: s[i]))]
    tr = pts[int(max(range(4), key=lambda i: d[i]))]
    bl = pts[int(min(range(4), key=lambda i: d[i]))]

    # Return polygon traversal order: top-left, top-right, bottom-right, bottom-left
    ordered = (tl, tr, br, bl)

    if len(set(ordered)) != 4:
        msg = "Corners are ambiguous (duplicate points)"
        raise ValueError(msg)
    return ordered
