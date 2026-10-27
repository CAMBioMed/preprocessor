from pathlib import Path
from typing import ClassVar, override

import pytest

from preprocessor.core.serialization.photo import Photo
from tests.preprocessor.core.model.cls_PydanticModelTestBase import PydanticModelTestBase


class Test_Photo(PydanticModelTestBase[Photo]):
    fields_and_values: ClassVar[
        dict[
            str,
            tuple[
                object | None,
                list[object],
                list[tuple[object, object]],
                list[object],
            ],
        ]
    ] = {
        "id": (
            "test_photo",
            ["another_photo"],
            [("UPPERCASE_ID", "uppercase_id")],
            ["", "   "],
        ),
        "original_filename": (
            Path("photos/test_photo.jpg").resolve(),
            [Path("photos/another_photo.jpg").resolve()],
            [],
            [1],
        ),
        "width": (
            640,
            [1920],
            [("640", 640)],
            [0, -1],
        ),
        "height": (
            480,
            [1080],
            [("480", 480)],
            [0, -1],
        ),
        "metadata": (
            {},
            [{"partner": "SZN", "camera": "EOS R5", "captured_on": "2025-08-27"}],
            [],
            [["not", "metadata"]],
        ),
        "quadrat": (
            None,
            [((0.0, 0.0), (640.0, 0.0), (640.0, 480.0), (0.0, 480.0))],
            [
                (
                    [
                        {"x": 0, "y": 0},
                        {"x": 640, "y": 0},
                        {"x": 640, "y": 480},
                        {"x": 0, "y": 480},
                    ],
                    ((0.0, 0.0), (640.0, 0.0), (640.0, 480.0), (0.0, 480.0)),
                )
            ],
            [[], [(0, 0), (640, 0), (640, 480)]],
        ),
    }
    """Map fields to initial, valid, normalized, and invalid values."""

    @override
    def create_model(self) -> Photo:
        """Create a valid photo using the current project-file schema."""

        return Photo(
            id="test_photo",
            original_filename=Path("photos/test_photo.jpg").resolve(),
            width=640,
            height=480,
            metadata={},
        )

    @override
    def update_model(self, model: Photo, field_name: str, new_value: object) -> Photo:
        """Return ``model`` with ``field_name`` updated through Pydantic validation."""

        values = model.model_dump(mode="python")
        values[field_name] = new_value
        return Photo.model_validate(values)

    @pytest.mark.parametrize(
        ("field_name", "initial_value", "new_value"),
        [(name, initial, value) for name, (initial, values, _, _) in fields_and_values.items() for value in values],
    )
    def test_should_preserve_valid_property_value_when_model_is_updated(
        self,
        field_name: str,
        initial_value: object,
        new_value: object,
    ) -> None:
        """Should preserve a valid property value when the model is updated."""

        self.assert_property_valid_value(field_name, initial_value, new_value)

    @pytest.mark.parametrize(
        ("field_name", "initial_value", "invalid_value"),
        [(name, initial, value) for name, (initial, _, _, values) in fields_and_values.items() for value in values],
    )
    def test_should_reject_invalid_property_value_when_model_is_updated(
        self,
        field_name: str,
        initial_value: object,
        invalid_value: object,
    ) -> None:
        """Should reject an invalid property value when the model is updated."""

        self.assert_property_invalid_value(field_name, initial_value, invalid_value)

    @pytest.mark.parametrize(
        ("field_name", "initial_value", "input_value", "expected_value"),
        [
            (name, initial, input_value, expected_value)
            for name, (initial, _, values, _) in fields_and_values.items()
            for input_value, expected_value in values
        ],
    )
    def test_should_normalize_property_value_when_model_is_updated(
        self,
        field_name: str,
        initial_value: object,
        input_value: object,
        expected_value: object,
    ) -> None:
        """Should normalize a property value when the model is updated."""

        self.assert_property_normalization(field_name, initial_value, input_value, expected_value)

    def test_should_group_photos_by_site_area_year_season_and_transect(self) -> None:
        """Should group photos by site, area, year, season, and transect."""

        # Arrange
        photos = [
            Photo(
                id="first",
                original_filename=Path("photos/first.jpg").resolve(),
                width=640,
                height=480,
                metadata={
                    "site": "site-a",
                    "area": "area-a",
                    "date": "2025-01-01",
                    "season": "summer",
                    "transect": "1",
                },
            ),
            Photo(
                id="second",
                original_filename=Path("photos/second.jpg").resolve(),
                width=640,
                height=480,
                metadata={
                    "site": "site-a",
                    "area": "area-a",
                    "date": "2025-12-31T23:59:59",
                    "season": "summer",
                    "transect": "1",
                    "camera": "different",
                },
            ),
            Photo(
                id="different-site",
                original_filename=Path("photos/different-site.jpg").resolve(),
                width=640,
                height=480,
                metadata={
                    "site": "site-b",
                    "area": "area-a",
                    "date": "2025-01-01",
                    "season": "summer",
                    "transect": "1",
                },
            ),
            Photo(
                id="different-area",
                original_filename=Path("photos/different-area.jpg").resolve(),
                width=640,
                height=480,
                metadata={
                    "site": "site-a",
                    "area": "area-b",
                    "date": "2025-01-01",
                    "season": "summer",
                    "transect": "1",
                },
            ),
            Photo(
                id="different-year",
                original_filename=Path("photos/different-year.jpg").resolve(),
                width=640,
                height=480,
                metadata={
                    "site": "site-a",
                    "area": "area-a",
                    "date": "2026-01-01",
                    "season": "summer",
                    "transect": "1",
                },
            ),
            Photo(
                id="different-season",
                original_filename=Path("photos/different-season.jpg").resolve(),
                width=640,
                height=480,
                metadata={
                    "site": "site-a",
                    "area": "area-a",
                    "date": "2025-01-01",
                    "season": "winter",
                    "transect": "1",
                },
            ),
            Photo(
                id="different-transect",
                original_filename=Path("photos/different-transect.jpg").resolve(),
                width=640,
                height=480,
                metadata={
                    "site": "site-a",
                    "area": "area-a",
                    "date": "2025-01-01",
                    "season": "summer",
                    "transect": "2",
                },
            ),
        ]

        # Act
        groups = Photo.group_photos(photos)

        # Assert
        assert [[photo.id for photo in group] for group in groups] == [
            ["first", "second"],
            ["different-site"],
            ["different-area"],
            ["different-year"],
            ["different-season"],
            ["different-transect"],
        ]

    def test_should_return_custom_filename_when_metadata_contains_filename(self) -> None:
        """Should return the configured custom filename."""

        # Arrange
        photo = self.create_model()
        photo.metadata = {"filename": "custom-name.tif"}

        # Act
        filename = photo.determine_filename(7)

        # Assert
        assert filename == "custom-name.tif"

    def test_should_generate_filename_from_metadata_when_filename_is_missing(self) -> None:
        """Should generate a filename from the photo metadata."""

        # Arrange
        photo = self.create_model()
        photo.original_filename = Path("photos/input.JPEG").resolve()
        photo.metadata = {
            "partner": "Partner",
            "area": "Area",
            "site": "Site",
            "date": "2025-08-27T14:30:00",
            "season": "Summer",
            "transect": "1",
        }

        # Act
        filename = photo.determine_filename(7)

        # Assert
        assert filename == "Partner_Area_Site_2025_Summer_1_2025-08-27_007.jpeg"

    def test_should_use_default_extension_and_omit_invalid_metadata_when_generating_filename(self) -> None:
        """Should use the default extension and omit invalid metadata values."""

        # Arrange
        photo = self.create_model()
        photo.original_filename = Path("photos/input").resolve()
        photo.metadata = {
            "partner": 123,
            "area": None,
            "site": "Site",
            "date": "not-a-date",
            "season": ["Summer"],
            "transect": "1",
        }

        # Act
        filename = photo.determine_filename(1)

        # Assert
        assert filename == "Site_1_001.jpg"
