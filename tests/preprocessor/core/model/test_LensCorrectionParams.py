import pytest

from preprocessor.core.model import LensCorrectionParams

class Test_LensCorrectionParams:

    fields_initial_new = [
        ("camera_matrix", None, ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, 1.0))),
        ("coefficients", None, [0.01, -0.02, 0.0, 0.0]),
    ]

    fields_name_invalid = [
        ("camera_matrix", "foo", "should be a valid tuple"),
        ("camera_matrix", ((1000.0, 0.0), (0.0, 1000.0)), "Field required"),
        ("coefficients", "foo", "should be a valid list"),
        ("coefficients", [0.01, -0.02], "should have at least 4 items"),
        ("coefficients", [0.01] * 15, "should have at most 14 items"),
        ("coefficients", [0.01, float("nan"), 0.0, 0.0], "must not contain NaN"),
    ]

    @pytest.mark.parametrize("field_name, initial_value, new_value", fields_initial_new)
    def test_properties_getter_setter_and_signals(
        self, field_name: str, initial_value: object, new_value: object
    ) -> None:
        """Model properties should have working getters, setters, and change signals."""
        # Arrange: empty MetadataModel
        params = LensCorrectionParams()

        # Assert: the initial value is as expected
        actual_value = getattr(params, field_name)
        assert actual_value == initial_value, \
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"

        # Act: update the model
        # We cannot use model_copy() here because it doesn't validate
        new_params = LensCorrectionParams.model_validate({**params.model_dump(), field_name: new_value})

        # Assert: the value is updated
        actual_value = getattr(new_params, field_name)
        assert actual_value == new_value, \
            f"After setting, value of {field_name} should be {new_value}, but got {actual_value}"

    @pytest.mark.parametrize("field_name, invalid_value, error_desc", fields_name_invalid)
    def test_properties_validation(self, field_name: str, invalid_value: object, error_desc: str) -> None:
        """Model properties should enforce type validation and constraints when set."""
        # Arrange
        params = LensCorrectionParams()

        # Assert: updating the model with an invalid value should fail
        with pytest.raises(ValueError, match=error_desc):
            # We cannot use model_copy() here because it doesn't validate
            LensCorrectionParams.model_validate({**params.model_dump(), field_name: invalid_value})

