import pytest

from preprocessor.core.serialization.crop_params import CropParams


class TestCropParams:
    """Tests for the CropParams class."""

    def test_should_order_quadrat_clockwise_when_corners_are_unsorted(self) -> None:
        """Should order valid corners from top-left clockwise."""

        # Arrange
        crop_params = CropParams(quadrat=((100, 100), (0, 0), (100, 0), (0, 100)))
        expected = ((0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0))

        # Act
        ordered = crop_params.quadrat_clockwise()

        # Assert
        assert ordered == expected
        assert crop_params.quadrat_tl == expected[0]
        assert crop_params.quadrat_tr == expected[1]
        assert crop_params.quadrat_br == expected[2]
        assert crop_params.quadrat_bl == expected[3]
        assert crop_params.quadrat_as_tuple() == expected

    def test_should_return_original_quadrat_when_quadrat_is_invalid(self) -> None:
        """Should return the original corners when the quadrat cannot be ordered."""

        # Arrange
        crop_params = CropParams(quadrat=((0, 0), (100, 0), (0, 100)))

        # Act / Assert
        with pytest.raises(ValueError, match="Expected exactly 4 points"):
            crop_params.quadrat_clockwise()
        assert crop_params.quadrat_as_tuple() == crop_params.quadrat

    def test_should_reject_duplicate_quadrat_corners_when_ordering(self) -> None:
        """Should reject duplicate corners when ordering the quadrat."""

        # Arrange
        crop_params = CropParams(quadrat=((0, 0), (100, 0), (100, 100), (100, 100)))

        # Act / Assert
        with pytest.raises(ValueError, match="Expected 4 distinct points"):
            crop_params.quadrat_clockwise()

    def test_should_reject_more_than_four_quadrat_corners(self) -> None:
        """Should reject a quadrat with more than four corners."""

        # Arrange / Act / Assert
        with pytest.raises(ValueError, match="at most 4"):
            CropParams(quadrat=((0, 0), (100, 0), (100, 100), (0, 100), (50, 50)))
