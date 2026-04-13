import textwrap
from datetime import datetime
from pathlib import Path
from typing import override, ClassVar

import pytest

from preprocessor.core.model import ProjectData, PhotoData, ColorCorrectionParams, LensCorrectionParams, CropParams, MetadataData
from preprocessor.core.type_corners import Corners
from tests.preprocessor.core.model.cls_PydanticModelTestBase import PydanticModelTestBase


class Test_ProjectData(PydanticModelTestBase):

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

    def test_to_json(self, tmp_path: Path) -> None:
        """to_json() should return a JSON string representation of the model.

        It should make absolute paths relative to the project directory.
        """
        # Arrange
        project_dir = tmp_path / "project"
        photos_dir = project_dir / "photos"  # Inside project dir
        export_dir = tmp_path / "export"  # Outside project dir
        model = ProjectData(
            photos=[
                PhotoData(
                    image_id="photo1",
                    image_path=photos_dir / "photo1.jpg",
                    color_correction=ColorCorrectionParams(),
                    lens_correction=LensCorrectionParams(coefficients=[0.01, -0.02, 0.001, 0.0005]),
                    crop=CropParams(corners=Corners(((1.0, 2.0), (3.0, 4.0)))),
                    metadata=MetadataData(partner="SZN", camera="EOS R5"),
                ),
            ],
            photos_path=photos_dir,
            export_path=export_dir,
        )

        # Act
        json_str = model.to_json(project_dir=project_dir)

        # Assert: the JSON string is not empty and contains expected keys
        assert json_str == textwrap.dedent(f"""\
        {{
          "photos": [
            {{
              "image_id": "photo1",
              "image_path": "photos/photo1.jpg",
              "color_correction": {{}},
              "lens_correction": {{
                "coefficients": [
                  0.01,
                  -0.02,
                  0.001,
                  0.0005
                ]
              }},
              "crop": {{
                "corners": [
                  [
                    1.0,
                    2.0
                  ],
                  [
                    3.0,
                    4.0
                  ]
                ]
              }},
              "metadata": {{
                "partner": "SZN",
                "camera": "EOS R5"
              }}
            }}
          ],
          "photos_path": "photos",
          "export_path": "{str(export_dir)}"
        }}""")

    def test_from_json(self, tmp_path: Path) -> None:
        """from_json() should create a model instance from a JSON string representation of the model."""
        # Arrange
        project_dir = tmp_path / "project"
        photos_dir = project_dir / "photos"  # Inside project dir
        export_dir = tmp_path / "export"  # Outside project dir
        json_str = textwrap.dedent(f"""\
        {{
          "photos": [
            {{
              "image_id": "photo1",
              "image_path": "photos/photo1.jpg",
              "color_correction": {{}},
              "lens_correction": {{
                "coefficients": [
                  0.01,
                  -0.02,
                  0.001,
                  0.0005
                ]
              }},
              "crop": {{
                "corners": [
                  [
                    1.0,
                    2.0
                  ],
                  [
                    3.0,
                    4.0
                  ]
                ]
              }},
              "metadata": {{
                "partner": "SZN",
                "camera": "EOS R5"
              }}
            }}
          ],
          "photos_path": "photos",
          "export_path": "{str(export_dir)}"
        }}""")

        # Act
        model = ProjectData.from_json(json_str=json_str, project_dir=project_dir)

        # Assert
        assert model == ProjectData(
            photos=[
                PhotoData(
                    image_id="photo1",
                    image_path=photos_dir / "photo1.jpg",
                    color_correction=ColorCorrectionParams(),
                    lens_correction=LensCorrectionParams(coefficients=[0.01, -0.02, 0.001, 0.0005]),
                    crop=CropParams(corners=Corners(((1.0, 2.0), (3.0, 4.0)))),
                    metadata=MetadataData(partner="SZN", camera="EOS R5"),
                ),
            ],
            photos_path=photos_dir,
            export_path=export_dir,
        )

    fields_and_values: ClassVar[dict[str, tuple[
        object | None,
        list[object],
        list[tuple[object, object]],
        list[object],
    ]]] = {
        "photos_path": (
            # Initial
            None,
            # Valid
            [
                Path("photos").resolve(),  # Absolute path
            ],
            # Normalized
            [
                (Path("photos/subdir"), Path("photos/subdir").resolve()),  # Relative path to absolute path
            ],
            # Invalid
            [
                3,  # Not a path
            ]
        ),
        "export_path": (
            # Initial
            None,
            # Valid
            [
                Path("export").resolve(),  # Absolute path
            ],
            # Normalized
            [
                (Path("export/subdir"), Path("export/subdir").resolve()),  # Relative path to absolute path
            ],
            # Invalid
            [
                6,  # Not a path
            ]
        ),
    }
    """Map for each field name to:
    - the default value,
    - a list of valid values,
    - a list of pairs: unnormalized value to normalized value,
    - a list of invalid values
    """

    @override
    def create_model(self) -> ProjectData:
        return ProjectData()

    @override
    def update_model(self, model: ProjectData, field_name: str, new_value: object) -> ProjectData:
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

    def test_write_to_csv_file(self, tmp_path: Path) -> None:
        # Arrange
        project_dir = tmp_path / "project"
        photos_dir = project_dir / "photos"  # Inside project dir
        export_dir = tmp_path / "export"  # Outside project dir
        project = ProjectData(
            photos=[
                PhotoData(
                    image_id="photo1",
                    image_path=photos_dir / "photo1.jpg",
                    metadata=MetadataData(
                        filename="testfile1.jpg",
                        partner="SZN",
                        camera="EOS R5",
                    ),
                ),
                PhotoData(
                    image_id="photo2",
                    image_path=photos_dir / "photo2.jpg",
                    metadata=MetadataData(
                        filename="testfile2.jpg",
                        date=datetime.fromisoformat("2023-09-01T12:00:00Z"),
                        partner="Aegean",
                        area="Crete",
                        site="Site1",
                        season="Fall",
                        transect="Transect1",
                        height=100,
                        latitude=35.0,
                        longitude=25.0,
                        depth="10m",
                        camera="Nikon D850",
                        photographer="John Doe",
                        water_quality="Clear",
                        strobes="Strobe1",
                        framing="Framing1",
                        white_balance_card="Card1",
                        comments="No comments",
                    )
                )
            ],
            photos_path=photos_dir,
            export_path=export_dir,
        )

        # Act
        csv_file = tmp_path / "output.csv"
        project.write_to_csv_file(csv_file)

        # Assert
        assert csv_file.exists(), "CSV file should be created"
        with csv_file.open("r", encoding="utf-8") as f:
            content = f.read()
        expected_content = textwrap.dedent("""\
        Name,Date,Partner,Area,Site,Season,Transect,Height (cm),Latitude,Longitude,Depth,Camera,Photographer,Water quality,Strobes,Framing gear used,White balance card,Comments
        testfile1.jpg,,SZN,,,,,,,,,EOS R5,,,,,,
        testfile2.jpg,2023-09-01,Aegean,Crete,Site1,Fall,Transect1,100,35.0,25.0,10m,Nikon D850,John Doe,Clear,Strobe1,Framing1,Card1,No comments
        """)
        assert content == expected_content

