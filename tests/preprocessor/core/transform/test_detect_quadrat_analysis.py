import copy
import math

import numpy as np
import pytest

from preprocessor.core.transform.detect_quadrat_analysis import DetectQuadratAnalysisJob, defaultParams
from preprocessor.core.types import ImageRGB, Line


@pytest.mark.parametrize("count", [0, 1, 2, 3])
def test_should_return_no_corners_when_fewer_than_four_candidates_exist(count: int) -> None:
    """Should return no corners when fewer than four candidates exist."""
    # Arrange
    debug_image = np.zeros((64, 64, 3), dtype=np.uint8)
    lines = [Line(10, 0), *(Line(10 * (i + 1), math.pi / 2) for i in range(count))]

    # Act
    corners = DetectQuadratAnalysisJob._find_corners(lines, debug_image)

    # Assert
    assert corners == []


def test_should_return_scaled_corners_when_four_rectangle_intersections_exist() -> None:
    """Should return scaled corners when four rectangle intersections exist."""
    # Arrange
    debug_image = np.zeros((64, 64, 3), dtype=np.uint8)
    lines = [Line(10, 0), Line(50, 0), Line(10, math.pi / 2), Line(50, math.pi / 2)]

    # Act
    corners = DetectQuadratAnalysisJob._find_corners(lines, debug_image, scale=0.5)

    # Assert
    assert corners == [(20, 20), (100, 20), (100, 100), (20, 100)]


def test_should_return_empty_corners_when_image_has_no_detectable_lines() -> None:
    """Should return empty corners when image has no detectable lines."""
    # Arrange
    image = ImageRGB.from_rgb_array(np.zeros((64, 64, 3), dtype=np.uint8))
    job = DetectQuadratAnalysisJob(image, copy.deepcopy(defaultParams))

    # Act
    result = job()

    # Assert
    assert result.as_tuple() == ()
    assert not result.is_valid()
