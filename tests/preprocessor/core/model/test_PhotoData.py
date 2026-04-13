from pathlib import Path

import pytest

from preprocessor.core.model import PhotoData, ColorCorrectionParams, LensCorrectionParams, CropParams, MetadataData
from preprocessor.core.type_corners import Corners


class Test_PhotoData:

    fields_initial_new = [
        ("color_correction", None, ColorCorrectionParams()),
        ("lens_correction", None, LensCorrectionParams(coefficients=[0.01, -0.02, 0.001, 0.0005])),
        ("crop", None, CropParams(corners=Corners(((1.0, 2.0), (3.0, 4.0))))),
        ("metadata", MetadataData(), MetadataData(partner="SZN", camera="EOS R5")),
    ]

    fields_invalid_errormsg = [
        ("color_correction", "foo", "instance of ColorCorrectionParams"),
        ("lens_correction", "foo", "instance of LensCorrectionParams"),
        ("crop", "foo", "instance of CropParams"),
        ("metadata", "foo", "instance of MetadataData"),
    ]

    @pytest.mark.parametrize("field_name, initial_value, new_value", fields_initial_new)
    def test_properties_getter_setter_and_signals(
        self, field_name: str, initial_value: object, new_value: object
    ) -> None:
        """Model properties should have working getters, setters, and change signals."""
        # Arrange: empty MetadataModel
        model = PhotoData(
            image_id="test_photo",
            image_path=Path("photos/test_photo.jpg").resolve(),
        )

        # Assert: the initial value is as expected
        actual_value = getattr(model, field_name)
        assert actual_value == initial_value, \
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"

        # Act: update the model
        setattr(model, field_name, new_value)

        # Assert: the value is updated
        actual_value = getattr(model, field_name)
        assert actual_value == new_value, \
            f"After setting, value of {field_name} should be {new_value}, but got {actual_value}"

    @pytest.mark.parametrize("field_name, invalid_value, error_desc", fields_invalid_errormsg)
    def test_properties_validation(self, field_name: str, invalid_value: object, error_desc: str) -> None:
        """Model properties should enforce type validation and constraints when set."""
        # Arrange
        model = PhotoData(
            image_id="test_photo",
            image_path=Path("photos/test_photo.jpg").resolve(),
        )

        # Assert: updating the model with an invalid value should fail
        with pytest.raises(ValueError, match=error_desc):
            setattr(model, field_name, invalid_value)

