from pathlib import Path

import pytest

from preprocessor.core.model import ProjectData, PhotoData, ColorCorrectionParams, LensCorrectionParams, CropParams, MetadataData
from preprocessor.core.type_corners import Corners


class Test_ProjectData:

    def test_photos_property(self) -> None:
        """The photos property should be a list of PhotoData objects."""
        # Arrange
        model = ProjectData()

        # Assert: the initial value is an empty list
        assert model.photos == [], f"Initial value of photos should be [], but got {model.photos}"

        # Act: update the model with a new list of photos
        new_photos = [
            PhotoData(
                image_id="photo1",
                image_path=Path("photos/photo1.jpg").resolve(),
                color_correction=ColorCorrectionParams(),
                lens_correction=LensCorrectionParams(coefficients=[0.01, -0.02, 0.001, 0.0005]),
                crop=CropParams(corners=Corners(((1.0, 2.0), (3.0, 4.0)))),
                metadata=MetadataData(partner="SZN", camera="EOS R5"),
            ),
            PhotoData(
                image_id="photo2",
                image_path=Path("photos/photo2.jpg").resolve(),
            ),
        ]
        new_model = ProjectData.model_validate({**model.model_dump(), "photos": new_photos})

        # Assert: the photos property is updated correctly
        assert new_model.photos == new_photos, f"After setting, photos should be {new_photos}, but got {new_model.photos}"

    fields_initial_new = [
        ("photos_path", None, Path("photos").resolve()),
        ("export_path", None, Path("export").resolve()),
    ]

    fields_invalid_errormsg = [
        ("photos_path", 3, "not a valid path"),
        ("export_path", 6, "not a valid path"),
    ]

    @pytest.mark.parametrize("field_name, initial_value, new_value", fields_initial_new)
    def test_properties_getter_setter_and_signals(
        self, field_name: str, initial_value: object, new_value: object
    ) -> None:
        """Model properties should have working getters, setters, and change signals."""
        # Arrange: empty MetadataModel
        model = ProjectData()

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
        model = ProjectData()

        # Assert: updating the model with an invalid value should fail
        with pytest.raises(ValueError, match=error_desc):
            setattr(model, field_name, invalid_value)

