from datetime import datetime
from pathlib import Path
from typing import override, ClassVar

import pytest

from preprocessor.core.model import PhotoData, ColorCorrectionParams, LensCorrectionParams, CropParams, MetadataData
from preprocessor.core.type_corners import Corners
from tests.preprocessor.core.model.cls_PydanticModelTestBase import PydanticModelTestBase


class Test_PhotoData(PydanticModelTestBase):
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
        "color_correction": (
            # Initial
            ColorCorrectionParams(),
            # Valid
            [
                ColorCorrectionParams(
                    enabled=True,
                    gain_r=0.1,
                    gain_g=-0.1,
                ),
            ],
            # Normalized
            [],
            # Invalid
            [
                "foo",
            ],
        ),
        "lens_correction": (
            # Initial
            LensCorrectionParams(),
            # Valid
            [
                LensCorrectionParams(
                    enabled=True,
                    coefficients=[0.01, -0.02, 0.001, 0.0005],
                ),
            ],
            # Normalized
            [],
            # Invalid
            ["foo"],
        ),
        "crop": (
            # Initial
            CropParams(),
            # Valid
            [
                CropParams(
                    enabled=True,
                    corners=Corners(((1.0, 2.0), (3.0, 4.0))),
                ),
            ],
            # Normalized
            [],
            # Invalid
            ["foo"],
        ),
        "metadata": (
            # Initial
            MetadataData(),
            # Valid
            [
                MetadataData(
                    partner="SZN",
                    camera="EOS R5",
                ),
            ],
            # Normalized
            [],
            # Invalid
            ["foo"],
        ),
    }
    """Map for each field name to:
    - the default value,
    - a list of valid values,
    - a list of pairs: unnormalized value to normalized value,
    - a list of invalid values
    """

    @override
    def create_model(self) -> PhotoData:
        return PhotoData(
            image_id="test_photo",
            original_filename=Path("photos/test_photo.jpg").resolve(),
        )

    @override
    def update_model(self, model: PhotoData, field_name: str, new_value: object) -> PhotoData:
        setattr(model, field_name, new_value)
        return model

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
        self.assert_property_valid_value(field_name, initial_value, new_value)

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
        self.assert_property_invalid_value(field_name, initial_value, invalid_value)

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
        self.assert_property_normalization(field_name, initial_value, input_value, expected_value)

    photos = [
        (
            "CSIC_Montgri_Dui_2025_Summer_1_2025-08-27_001.jpg",
            PhotoData(
                image_id="img_001",
                original_filename=Path("img_001.jpg").resolve(),
                metadata=MetadataData(
                    date=datetime(2025, 8, 27),
                    partner="CSIC",
                    area="Montgri",
                    site="Dui",
                    season="Summer",
                    transect="1",
                    depth="5",
                    camera="NIKON D7000",
                ),
            ),
        ),
        (
            "CSIC_Montgri_Dui_2025_Summer_1_2025-08-27_002.jpg",
            PhotoData(
                image_id="img_002",
                original_filename=Path("img_002.jpg").resolve(),
                metadata=MetadataData(
                    date=datetime(2025, 8, 27),
                    partner="CSIC",
                    area="Montgri",
                    site="Dui",
                    season="Summer",
                    transect="1",
                    depth="5",
                    camera="NIKON D7000",
                ),
            ),
        ),
        (
            "CSIC_Montgri_Dui_2025_Summer_1_2025-08-28_003.jpg",
            PhotoData(
                image_id="img_003",
                original_filename=Path("img_003.jpg").resolve(),
                metadata=MetadataData(
                    date=datetime(2025, 8, 28),
                    partner="CSIC",
                    area="Montgri",
                    site="Dui",
                    season="Summer",
                    transect="1",
                    depth="5",
                    camera="NIKON D7000",
                ),
            ),
        ),
        (
            "CSIC_Montgri_Falaguer_2025_Summer_1_2025-08-27_001.jpg",
            PhotoData(
                image_id="img_004",
                original_filename=Path("img_004.jpg").resolve(),
                metadata=MetadataData(
                    date=datetime(2025, 8, 27),
                    partner="CSIC",
                    area="Montgri",
                    site="Falaguer",
                    season="Summer",
                    transect="1",
                    depth="5",
                    camera="NIKON D7000",
                ),
            ),
        ),
        (
            "CSIC_Medes_Portixol_2025_Summer_1_2025-08-27_001.jpg",
            PhotoData(
                image_id="img_005",
                original_filename=Path("img_005.jpg").resolve(),
                metadata=MetadataData(
                    date=datetime(2025, 8, 27),
                    partner="CSIC",
                    area="Medes",
                    site="Portixol",
                    season="Summer",
                    transect="1",
                    depth="5",
                    camera="NIKON D7000",
                ),
            ),
        ),
        (
            "CSIC_Montgri_Falaguer_2025_Summer_1_2025-08-27_002.jpg",
            PhotoData(
                image_id="img_006",
                original_filename=Path("img_006.jpg").resolve(),
                metadata=MetadataData(
                    date=datetime(2025, 8, 27),
                    partner="CSIC",
                    area="Montgri",
                    site="Falaguer",
                    season="Summer",
                    transect="1",
                    depth="5",
                    camera="NIKON D7000",
                ),
            ),
        ),
        (
            "CSIC_Medes_Portixol_2025_Summer_1_2025-08-27_002.jpg",
            PhotoData(
                image_id="img_007",
                original_filename=Path("img_007.jpg").resolve(),
                metadata=MetadataData(
                    date=datetime(2025, 8, 27),
                    partner="CSIC",
                    area="Medes",
                    site="Portixol",
                    season="Summer",
                    transect="1",
                    depth="5",
                    camera="NIKON D7000",
                ),
            ),
        ),
        (
            "custom_filename.jpg",
            PhotoData(
                image_id="img_008",
                original_filename=Path("img_008.jpg").resolve(),
                metadata=MetadataData(
                    filename="custom_filename.jpg",
                    date=datetime(2025, 8, 27),
                    partner="CSIC",
                    area="Medes",
                    site="Portixol",
                    season="Summer",
                    transect="1",
                    depth="5",
                    camera="NIKON D7000",
                ),
            ),
        ),
    ]

    def test_determine_filename(self) -> None:
        """Tests the group_photos() and determine_filename() function."""

        # Group the photos
        groups = PhotoData.group_photos(photo for _, photo in self.photos)

        # Check the expected filenames
        for group in groups:
            for idx, photo in enumerate(group):
                expected_filename = next(expected for expected, p in self.photos if p == photo)
                assert photo.determine_filename(idx + 1) == expected_filename
