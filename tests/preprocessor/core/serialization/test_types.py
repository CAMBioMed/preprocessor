from math import inf, nan

import pytest
from pydantic import BaseModel, ValidationError

from preprocessor.core.serialization import LensVector, Matrix3x3


class LensTypesDocument(BaseModel):
    """Test model carrying lens-correction type aliases."""

    coefficients: LensVector
    camera_matrix: Matrix3x3


def test_should_normalize_lens_types_to_float_collections_when_values_are_valid() -> None:
    """Should normalize valid lens vectors and matrices to their declared collections."""

    # Arrange
    document_data = {
        "coefficients": [1, -2, 0.5, 0],
        "camera_matrix": [[1000, 0, 512], [0, 1000, 384], [0, 0, 1]],
    }

    # Act
    document = LensTypesDocument.model_validate(document_data)

    # Assert
    assert document.coefficients == [1.0, -2.0, 0.5, 0.0]
    assert document.camera_matrix == ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, 1.0))


@pytest.mark.parametrize("value", [[0.0, nan, 0.0, 0.0], [0.0, inf, 0.0, 0.0]])
def test_should_reject_non_finite_lens_vector_values_when_validated(value: object) -> None:
    """Should reject non-finite lens-vector values."""

    # Arrange
    document_data = {
        "coefficients": value,
        "camera_matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    }

    # Act / Assert
    with pytest.raises(ValidationError, match="finite number"):
        LensTypesDocument.model_validate(document_data)


@pytest.mark.parametrize(
    "value",
    [
        [[1.0, 0.0], [0.0, 1.0]],
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, nan]],
    ],
)
def test_should_reject_invalid_matrix_values_when_validated(value: object) -> None:
    """Should reject non-3x3 or non-finite matrix values."""

    # Arrange
    document_data = {"coefficients": [0.0] * 4, "camera_matrix": value}

    # Act / Assert
    with pytest.raises(ValidationError):
        LensTypesDocument.model_validate(document_data)
