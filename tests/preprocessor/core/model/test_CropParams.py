import pytest

from preprocessor.core.model import LensCorrectionParams, CropParams
from preprocessor.core.type_corners import Corners


class Test_CropParams:

    fields_initial_new = [
        ("corners", Corners(()), Corners(((0.1, 0.2), (1.1, 0.2), (1.1, 1.2), (0.1, 1.2)))),
    ]

    fields_name_invalid = [
        ("corners", "foo", "should be a valid tuple"),
        ("corners", None, "should be a valid tuple"),
    ]

    @pytest.mark.parametrize("field_name, initial_value, new_value", fields_initial_new)
    def test_properties_getter_setter_and_signals(
        self, field_name: str, initial_value: object, new_value: object
    ) -> None:
        """Model properties should have working getters, setters, and change signals."""
        # Arrange: empty MetadataModel
        params = CropParams()

        # Assert: the initial value is as expected
        actual_value = getattr(params, field_name)
        assert actual_value == initial_value, \
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"

        # Act: update the model
        # We cannot use model_copy() here because it doesn't validate
        new_params = CropParams.model_validate({**params.model_dump(), field_name: new_value})

        # Assert: the value is updated
        actual_value = getattr(new_params, field_name)
        assert actual_value == new_value, \
            f"After setting, value of {field_name} should be {new_value}, but got {actual_value}"

    @pytest.mark.parametrize("field_name, invalid_value, error_desc", fields_name_invalid)
    def test_properties_validation(self, field_name: str, invalid_value: object, error_desc: str) -> None:
        """Model properties should enforce type validation and constraints when set."""
        # Arrange
        params = CropParams()

        # Assert: updating the model with an invalid value should fail
        with pytest.raises(ValueError, match=error_desc):
            # We cannot use model_copy() here because it doesn't validate
            CropParams.model_validate({**params.model_dump(), field_name: invalid_value})

