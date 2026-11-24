from math import inf, nan

import pytest
from pydantic import BaseModel

from preprocessor.core.serialization import Point2D


class PointDocument(BaseModel):
    """Test model carrying a Point2D value."""

    point: Point2D


@pytest.mark.parametrize(
    ("input_value", "expected_value"),
    [
        ((1, 2), (1.0, 2.0)),
        ({"x": 1, "y": 2}, (1.0, 2.0)),
    ],
)
def test_should_normalize_point_input_to_tuple_when_point_is_valid(
    input_value: object,
    expected_value: tuple[float, float],
) -> None:
    """Should normalize point input to a tuple when the point is valid."""
    # Arrange
    document_data = {"point": input_value}

    # Act
    document = PointDocument.model_validate(document_data)

    # Assert
    assert document.point == expected_value


def test_should_serialize_point_as_object_when_point_is_dumped() -> None:
    """Should serialize a point as an object when the point is dumped."""
    # Arrange
    document = PointDocument(point=(1.0, 2.0))
    expected_value = {"point": {"x": 1.0, "y": 2.0}}

    # Act
    python_dump = document.model_dump()
    json_dump = document.model_dump(mode="json")

    # Assert
    assert python_dump == expected_value
    assert json_dump == expected_value


@pytest.mark.parametrize(
    "input_value",
    [
        {"x": 1},
        {"y": 2},
        {"x": 1, "y": 2, "z": 3},
    ],
)
def test_should_reject_point_object_without_exact_x_and_y_keys_when_validated(input_value: object) -> None:
    """Should reject a point object without exactly x and y keys when validated."""
    # Arrange
    document_data = {"point": input_value}

    # Assert
    with pytest.raises(ValueError, match="point object must contain exactly 'x' and 'y'"):
        PointDocument.model_validate(document_data)


@pytest.mark.parametrize("input_value", [(nan, 0.0), (0.0, inf), (-inf, 0.0)])
def test_should_reject_non_finite_point_coordinates_when_validated(input_value: object) -> None:
    """Should reject non-finite point coordinates when validated."""
    # Arrange
    document_data = {"point": input_value}

    # Assert
    with pytest.raises(ValueError, match="finite number"):
        PointDocument.model_validate(document_data)
