import pytest
from pathlib import Path

from PySide6.QtCore import Slot
from pytestqt.qtbot import QtBot

from preprocessor.core.type_corners import Corners
from preprocessor.gui.model import QPhotoModel
from preprocessor.core.model import PhotoData, ColorCorrectionParams, LensCorrectionParams, CropParams, MetadataData
from tests.preprocessor.models.qmodel_fixture import (
    assert_has_a_property_for_each_data_field,
    assert_model_property_getter_setter_and_signal,
    assert_model_property_signals_on_mutation,
)


class Test_QPhotoModel:
    """Unit tests for QPhotoModel."""

    @staticmethod
    def create_test_model() -> QPhotoModel:
        """Helper to create a test PhotoModel with default values."""
        return QPhotoModel(
            PhotoData(
                image_path=Path("img_001.jpg").resolve(),
                image_id="img_001",
            )
        )

    def test_has_a_property_for_each_data_field(self) -> None:
        """Model should have a property for each field in the data model."""
        assert_has_a_property_for_each_data_field(QPhotoModel, PhotoData)

    fields_name_initial_new = [
        ("image_id", "img_001", "img_002"),
        ("image_path", Path("img_001.jpg").resolve(), Path("img_002.jpg").resolve()),
        # TODO:
        # ("color_correction", None, ColorCorrectionParams(
        #     [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        # )),
        ("lens_correction", None, LensCorrectionParams(
            camera_matrix = ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, 1.0)),
            coefficients = [0.01, -0.02, 0.0, 0.0],
        )),
        ("crop", None, CropParams(
            corners=Corners(((1.0, 2.0), (3.0, 4.0))),
        )),
        ("metadata", MetadataData(), MetadataData(
            site="MySite",
        )),
    ]

    @pytest.mark.parametrize("field_name, initial_value, new_value", fields_name_initial_new)
    def test_properties_getter_setter_and_signals(
        self, qtbot: QtBot, field_name: str, initial_value: object, new_value: object
    ) -> None:
        """Model properties should have working getters, setters, and change signals."""
        with qtbot.capture_exceptions():
            # Arrange: empty MetadataModel
            model = self.create_test_model()

            # Assert: fields signal correctly on change
            assert_model_property_getter_setter_and_signal(qtbot, model, field_name, initial_value, new_value)

    # noinspection PyTypeChecker
    fields_name_invalid = [
        # Invalid type
        ("image_id", 10),  # Invalid type
        ("image_path", 20),  # Invalid type
        ("color_correction", "not a ColorCorrectionParams"),  # Invalid type
        ("lens_correction", "not a LensCorrectionParams"),  # Invalid type
        ("crop", "not a CropParams"),  # Invalid type
        ("metadata", "not a MetadataData"),  # Invalid type
        # Too many values
        # TODO: Test these
        # ("crop", CropParams(
        #     corners=Corners(((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (2.0, 2.0))),
        # )),  # Too many corners
        # ("lens_correction", LensCorrectionParams(
        #     camera_matrix = ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0)),  # type: ignore[arg-type]
        # )),  # Camera matrix not 3x3
        # ("lens_correction", LensCorrectionParams(
        #     coefficients=[0.01, -0.02],
        # )),  # Too few coefficients
    ]

    @pytest.mark.parametrize("field_name, invalid_value", fields_name_invalid)
    def test_properties_validation(self, field_name: str, invalid_value: object) -> None:
        """Model properties should enforce type validation and constraints when set."""
        model = self.create_test_model()

        with pytest.raises(ValueError):
            setattr(model, field_name, invalid_value)

    fields_name_value_normalized = [
        # Paths are normalized
        ("image_path", str(Path("img_003.jpg").resolve()), Path("img_003.jpg").resolve()),  # str to Path
        # Empty lists become None
        # ("quadrat_corners", [], None),
    ]

    @pytest.mark.parametrize("field_name, input_value, expected_value", fields_name_value_normalized)
    def test_properties_normalization(self, field_name: str, input_value: object, expected_value: object) -> None:
        """Model properties should normalize (trimming, empty to None) on assignment."""
        model = self.create_test_model()

        # Act: set the value
        setattr(model, field_name, input_value)

        # Assert: the value is normalized as expected
        assert getattr(model, field_name) == expected_value

    def test_metadata_property_and_signal(self, qtbot: QtBot) -> None:
        """MetadataModel should be accessible and emit on_metadata_changed when modified."""
        with qtbot.capture_exceptions():
            model = self.create_test_model()

            # Assert: metadata is accessible
            assert model.metadata is not None

            initial_metadata = model.metadata
            new_metadata = initial_metadata.model_copy(update={"partner": "Acme Corp"})

            assert_model_property_signals_on_mutation(
                qtbot,
                model,
                "metadata",
                fn_set_same=lambda m, p: setattr(m, "metadata", initial_metadata),
                fn_set_new=lambda m, p: setattr(m, "metadata", new_metadata),
            )

    def test_serialize_deserialize(self, tmp_path: Path) -> None:
        # Arrange
        project_dir = tmp_path / "project"
        photo0 = QPhotoModel(
            PhotoData(
                image_id="img_001",
                image_path=project_dir / "img_001.jpg",
            )
        )

        # Assert: defaults set (quadrat_corners defaults to None)
        assert photo0.image_path == project_dir / "img_001.jpg"
        assert photo0.image_id == "img_001"
        assert photo0.color_correction is None
        assert photo0.lens_correction is None
        assert photo0.crop is None

        # Act: Serialize and deserialize
        json_str0: str = photo0._data.model_dump_json()
        photo1: QPhotoModel = QPhotoModel(PhotoData.model_validate_json(json_str0))

        # Assert: values read
        assert photo1.image_path == photo0.image_path
        assert photo1.image_id == photo0.image_id
        assert photo1.color_correction == photo0.color_correction
        assert photo1.lens_correction == photo0.lens_correction
        assert photo1.crop == photo0.crop

        # Act: Set some values
        color_correction = ColorCorrectionParams()
        lens_correction = LensCorrectionParams(
            camera_matrix=(
                (1000.0, 0.0, 512.0),
                (0.0, 1000.0, 384.0),
                (0.0, 0.0, 1.0),
            ),
            coefficients=[0.01, -0.02, 0.0, 0.0],
        )
        crop = CropParams(
            corners=Corners(((0.1, 0.2), (1.1, 0.2), (1.1, 1.2), (0.1, 1.2))),
        )
        photo1.image_path = project_dir / "img_001.jpg"
        photo1.image_id = "img_001"
        photo1.color_correction = color_correction
        photo1.lens_correction = lens_correction
        photo1.crop = crop

        # Assert: verify values set
        assert photo1.image_path == project_dir / "img_001.jpg"
        assert photo1.image_id == "img_001"
        assert photo1.color_correction == color_correction
        assert photo1.lens_correction == lens_correction
        assert photo1.crop == crop

        # Act: Serialize and deserialize
        json_str1: str = photo1._data.model_dump_json()
        photo2: QPhotoModel = QPhotoModel(PhotoData.model_validate_json(json_str1))

        # Assert: verify values read
        assert photo2.image_path == project_dir / "img_001.jpg"
        assert photo2.image_id == "img_001"
        assert photo2.color_correction == color_correction
        assert photo2.lens_correction == lens_correction
        assert photo2.crop == crop
