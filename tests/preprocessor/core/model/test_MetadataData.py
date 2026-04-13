from datetime import datetime, timezone, timedelta

import pytest

from preprocessor.core.model import MetadataData
from preprocessor.core.type_corners import Corners


class Test_MetadataData:

    fields_and_values: dict[str, tuple[object | None, list[object], list[tuple[object, object]], list[object]]] = {
        "filename": (
            # Initial
            None,
            # Valid
            [
                "Test-Name.jpg",
                "x" * 200,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  Test-Name.jpg  ", "Test-Name.jpg"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 201,  # Must be <= 200 chars
            ],
        ),
        "date": (
            # Initial
            None,
            # Valid
            [
                datetime(2026, 3, 24, 14, 0, 0),
            ],
            [
                ("", None),  # Empty string becomes None
                ("2016-05-30", datetime(2016, 5, 30, 0, 0, 0)),
                ("2016-05-30T15:46:24", datetime(2016, 5, 30, 15, 46, 24)),
                (
                    "2025-09-20T16:35:48.429000+02:00",
                    datetime(2025, 9, 20, 16, 35, 48, 429000, tzinfo=timezone(timedelta(seconds=7200))),
                ),
                (
                    "2025-05-04T13:17:58+01:00",
                    datetime(2025, 5, 4, 13, 17, 58, tzinfo=timezone(timedelta(seconds=3600))),
                ),
                ("2025-12-15T10:30:00Z", datetime(2025, 12, 15, 10, 30, 0, tzinfo=timezone.utc)),
                ("  2026-03-24T14:00:00  ", datetime(2026, 3, 24, 14, 0, 0)),  # Trims whitespace
            ],
            # Invalid
            [
                "not a date",  # Invalid type
            ],
        ),
        "partner": (
            # Initial
            None,
            # Valid
            [
                "Acme Corp",
                "x" * 50,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  Acme Corp  ", "Acme Corp"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 51,  # Must be <= 50 chars
            ],
        ),
        "area": (
            # Initial
            None,
            # Valid
            [
                "Coral Reef",
                "x" * 50,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  Coral Reef  ", "Coral Reef"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 51,  # Must be <= 50 chars
            ],
        ),
        "site": (
            # Initial
            None,
            # Valid
            [
                "Site A",
                "x" * 50,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  Site A  ", "Site A"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 51  # Must be <= 50 chars
            ],
        ),
        "season": (
            # Initial
            None,
            # Valid
            [
                "Spring",
                "x" * 50,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  Spring  ", "Spring"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 51  # Must be <= 50 chars
            ],
        ),
        "transect": (
            # Initial
            None,
            # Valid
            [
                "Transect 1",
                "x" * 50,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                ("  Transect 1  ", "Transect 1"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 51  # Must be <= 50 chars
            ],
        ),
        "height": (
            # Initial
            None,
            # Valid
            [
                10000,
                0,
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" 10 ", 10),  # Trims whitespace and converts to int
            ],
            # Invalid
            [
                "not a number",  # Invalid type
                -100,  # Must be >= 0
            ],
        ),
        "latitude": (
            # Initial
            None,
            # Valid
            [
                34.0522,
                -90.0,
                90.0,
                0.0,
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" 34.0522 ", 34.0522),  # Trims whitespace and converts to float
            ],
            # Invalid
            [
                "not a number",  # Invalid type
                100.0,  # Must be <= 90
                -100.0,  # Must be >= -90
            ],
        ),
        "longitude": (
            # Initial
            None,
            # Valid
            [
                -118.2437,
                -180.0,
                180.0,
                0.0,
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" -118.2437 ", -118.2437),  # Trims whitespace and converts to float
            ],
            # Invalid
            [
                "not a number",  # Invalid type
                200.0,  # Must be <= 180
                -200.0,  # Must be >= -180
            ],
        ),
        "depth": (
            # Initial
            None,
            # Valid
            [
                "20m",
                "x" * 45,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" 20m ", "20m"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 46,  # Must be <= 45 chars
            ],
        ),
        "camera": (
            # Initial
            None,
            # Valid
            [
                "Canon EOS R5",
                "x" * 200,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" Canon EOS R5 ", "Canon EOS R5"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 201,  # Must be <= 200 chars
            ],
        ),
        "photographer": (
            # Initial
            None,
            # Valid
            [
                "Jane Doe",
                "x" * 45,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" Jane Doe ", "Jane Doe"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 46,  # Must be <= 45 chars
            ],
        ),
        "water_quality": (
            # Initial
            None,
            # Valid
            [
                "Clear",
                "x" * 45,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" Clear ", "Clear"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 46,  # Must be <= 45 chars
            ],
        ),
        "strobes": (
            # Initial
            None,
            # Valid
            [
                "Yes",
                "x" * 200,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" Yes ", "Yes"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 201,  # Must be <= 200 chars
            ],
        ),
        "framing": (
            # Initial
            None,
            # Valid
            [
                "Tight",
                "x" * 200,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" Tight ", "Tight"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 201,  # Must be <= 200 chars
            ],
        ),
        "white_balance_card": (
            # Initial
            None,
            # Valid
            [
                "Yes",
                "x" * 200,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" Yes ", "Yes"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 201,  # Must be <= 200 chars
            ],
        ),
        "comments": (
            # Initial
            None,
            # Valid
            [
                "No issues",
                "x" * 1000,  # Max length
            ],
            # Normalized
            [
                ("", None),  # Empty string becomes None
                (" No issues ", "No issues"),  # Trims whitespace
            ],
            # Invalid
            [
                "x" * 1001,  # Must be <= 1000 chars
            ],
        ),
    }
    """Map for each field name to:
    - the default value,
    - a list of valid values,
    - a list of pairs: unnormalized value to normalized value,
    - a list of invalid values
    """

    def create_model(self) -> MetadataData:
        return MetadataData()

    def update_model(self, model: MetadataData, field_name: str, new_value: object) -> MetadataData:
        """Updates the specified field of the specified model and returns the new model
        (or the same model if the update was in-place)."""
        # We cannot use model_copy() here because it doesn't validate
        new_model = MetadataData.model_validate({**model.model_dump(), field_name: new_value})
        return new_model

    @pytest.mark.parametrize(
        "field_name, initial_value, new_value",
        [(n, v, vv) for n, (v, vvs, _, _) in fields_and_values.items() for vv in vvs],
    )
    def test_property_valid_value(
        self,
        field_name: str,
        initial_value: object,
        new_value: object,
    ) -> None:
        """Model properties can be set to a valid value."""
        # Arrange: empty model
        model = self.create_model()

        # Assert: the initial value is as expected
        actual_value = getattr(model, field_name)
        assert actual_value == initial_value, \
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"

        # Act: update the model
        new_model = self.update_model(model, field_name, new_value)

        # Assert: the value is updated
        actual_value = getattr(new_model, field_name)
        assert actual_value == new_value, \
            f"After setting, value of {field_name} should be {new_value}, but got {actual_value}"

    @pytest.mark.parametrize(
        "field_name, initial_value, invalid_value",
        [(n, v, iv) for n, (v, _, _, ivs) in fields_and_values.items() for iv in ivs],
    )
    def test_property_invalid_value(
        self,
        field_name: str,
        initial_value: object,
        invalid_value: object,
    ) -> None:
        """Model properties should enforce type validation and constraints when set."""
        # Arrange: empty model
        model = self.create_model()

        # Assert: the initial value is as expected
        actual_value = getattr(model, field_name)
        assert actual_value == initial_value, \
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"

        # Assert: updating the model with an invalid value should fail
        with pytest.raises(ValueError):
            self.update_model(model, field_name, invalid_value)

    @pytest.mark.parametrize(
        "field_name, initial_value, input_value, expected_value",
        [(n, v, lv, rv) for n, (v, _, nvs, _) in fields_and_values.items() for (lv, rv) in nvs],
    )
    def test_property_normalization(
        self,
        field_name: str,
        initial_value: object,
        input_value: object,
        expected_value: object,
    ) -> None:
        """Model properties should normalize (trimming, empty to None) on assignment."""
        # Arrange: empty model
        model = self.create_model()

        # Assert: the initial value is as expected
        actual_value = getattr(model, field_name)
        assert actual_value == initial_value, \
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"

        # Act: set the value
        new_model = self.update_model(model, field_name, input_value)

        # Assert: the value is normalized as expected
        assert getattr(new_model, field_name) == expected_value
