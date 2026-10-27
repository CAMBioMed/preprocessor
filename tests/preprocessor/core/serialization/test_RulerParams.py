from math import inf, nan

import pytest
from pydantic import ValidationError

from preprocessor.core.serialization.ruler_params import RulerParams


class TestRulerParams:
    """Tests for the RulerParams class."""

    def test_should_default_to_disabled_with_no_points(self) -> None:
        """Should default to a disabled ruler with no points."""

        # Arrange / Act
        ruler_params = RulerParams()

        # Assert
        assert ruler_params.enabled is False
        assert ruler_params.points == ()

    def test_should_normalize_valid_point_values_to_finite_tuples(self) -> None:
        """Should normalize valid point values to tuples of floats."""
        # Arrange
        ruler_params = RulerParams.model_validate(
            {
                "enabled": True,
                "points": [{"x": 1, "y": 2}, (3, 4)],
            }
        )

        # Act
        points = ruler_params.points

        # Assert
        assert points == ((1.0, 2.0), (3.0, 4.0))

    def test_should_serialize_points_as_objects_when_model_is_dumped(self) -> None:
        """Should serialize ruler points as x/y objects."""

        # Arrange
        ruler_params = RulerParams(enabled=True, points=((1.0, 2.0), (3.0, 4.0)))

        # Act
        dumped = ruler_params.model_dump(mode="json")

        # Assert
        assert dumped == {
            "enabled": True,
            "points": [{"x": 1.0, "y": 2.0}, {"x": 3.0, "y": 4.0}],
        }

    def test_should_reject_more_than_two_points_when_validating(self) -> None:
        """Should reject more than two ruler points."""

        # Arrange / Act / Assert
        with pytest.raises(ValidationError, match="at most 2 items"):
            RulerParams(points=((0, 0), (1, 1), (2, 2)))

    @pytest.mark.parametrize(
        "points",
        [
            ((nan, 0),),
            ((inf, 0),),
            ((0, 0), {"x": 1}),
        ],
    )
    def test_should_reject_invalid_points_when_validating(self, points: object) -> None:
        """Should reject malformed or non-finite ruler points."""

        # Arrange / Act / Assert
        with pytest.raises(ValidationError):
            RulerParams.model_validate({"points": points})

    def test_should_reject_assignment_when_model_is_frozen(self) -> None:
        """Should reject assignment to a frozen ruler model."""

        # Arrange
        ruler_params = RulerParams()

        # Act / Assert
        with pytest.raises(ValidationError, match="frozen"):
            ruler_params.enabled = True
