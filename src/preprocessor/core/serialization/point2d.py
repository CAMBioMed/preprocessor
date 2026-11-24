"""Finite 2D points with object-shaped JSON serialization."""

from collections.abc import Mapping
from typing import Annotated, cast

from pydantic import BeforeValidator, FiniteFloat, PlainSerializer


def _validate_point(value: object) -> object:
    """Convert an object-shaped point to its tuple representation."""
    if isinstance(value, Mapping):
        point = cast(Mapping[str, object], value)
        if set(point) != {"x", "y"}:
            msg = "point object must contain exactly 'x' and 'y'"
            raise ValueError(msg)
        return (point["x"], point["y"])
    return value


def _serialize_point(point: tuple[float, float]) -> dict[str, float]:
    """Serialize a point as an object with horizontal and vertical coordinates."""

    return {"x": point[0], "y": point[1]}


type Point2D = Annotated[
    tuple[FiniteFloat, FiniteFloat],
    BeforeValidator(_validate_point),
    PlainSerializer(_serialize_point, return_type=dict[str, float]),
]
"""A finite 2D point of an x and y coordinate."""
