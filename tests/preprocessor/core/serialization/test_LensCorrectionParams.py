from math import inf, nan

import pytest
from pydantic import ValidationError

from preprocessor.core.serialization.lens_correction_params import LensCorrectionParams


class TestLensCorrectionParams:
    """Tests for the LensCorrectionParams class."""

    def test_should_default_to_disabled_without_lens_values(self) -> None:
        """Should default to disabled without camera values or coefficients."""

        # Arrange / Act
        params = LensCorrectionParams()

        # Assert
        assert params.enabled is False
        assert params.camera_matrix is None
        assert params.coefficients is None

    def test_should_normalize_valid_lens_values_when_validated(self) -> None:
        """Should normalize valid camera and coefficient values."""

        # Arrange / Act
        params = LensCorrectionParams.model_validate(
            {
                "enabled": True,
                "camera_matrix": [[1000, 0, 512], [0, 1000, 384], [0, 0, 1]],
                "coefficients": (0.1, -0.2, 0.0, 0.01),
            }
        )

        # Assert
        assert params.camera_matrix == ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, 1.0))
        assert params.coefficients == [0.1, -0.2, 0.0, 0.01]

    def test_should_serialize_lens_values_as_json_arrays_when_dumped(self) -> None:
        """Should serialize lens values as JSON-compatible arrays."""

        # Arrange
        params = LensCorrectionParams(
            enabled=True,
            camera_matrix=((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, 1.0)),
            coefficients=[0.1, -0.2, 0.0, 0.01],
        )

        # Act
        dumped = params.model_dump(mode="json")

        # Assert
        assert dumped == {
            "enabled": True,
            "camera_matrix": [[1000.0, 0.0, 512.0], [0.0, 1000.0, 384.0], [0.0, 0.0, 1.0]],
            "coefficients": [0.1, -0.2, 0.0, 0.01],
        }

    @pytest.mark.parametrize(
        "value",
        [
            ((1000.0, 0.0), (0.0, 1000.0)),
            ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, nan)),
            ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, inf)),
        ],
    )
    def test_should_reject_invalid_camera_matrix_when_validated(self, value: object) -> None:
        """Should reject malformed or non-finite camera matrices."""

        # Arrange / Act / Assert
        with pytest.raises(ValidationError):
            LensCorrectionParams.model_validate({"camera_matrix": value})

    @pytest.mark.parametrize(
        "value",
        [
            [0.0, 0.0],
            [0.0] * 6,
            [0.0] * 15,
            [0.0, nan, 0.0, 0.0],
            [0.0, inf, 0.0, 0.0],
        ],
    )
    def test_should_reject_invalid_coefficients_when_validated(self, value: object) -> None:
        """Should reject unsupported or non-finite distortion coefficients."""

        # Arrange / Act / Assert
        with pytest.raises(ValidationError):
            LensCorrectionParams.model_validate({"coefficients": value})

    def test_should_reject_assignment_when_model_is_frozen(self) -> None:
        """Should reject assignment to a frozen lens correction model."""

        # Arrange
        params = LensCorrectionParams()

        # Act / Assert
        with pytest.raises(ValidationError, match="frozen"):
            params.enabled = True
