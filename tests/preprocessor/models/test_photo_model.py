import pytest
from pathlib import Path

from PySide6.QtCore import Slot
from pytestqt.qtbot import QtBot

from preprocessor.model.photo_model import PhotoModel, PhotoData
from tests.preprocessor.models.qmodel_fixture import (
    assert_has_a_property_for_each_data_field,
    assert_model_property_getter_setter_and_signal,
    assert_model_property_signals_on_mutation,
)


class TestPhotoModel:
    """Unit tests for PhotoModel and PhotoData."""

    @staticmethod
    def create_test_model() -> PhotoModel:
        """Helper to create a test PhotoModel with default values."""
        return PhotoModel(
            PhotoData(
                original_filename=Path("img_001.jpg"),
                width=1024,
                height=768,
            )
        )

    def test_has_a_property_for_each_data_field(self) -> None:
        """Model should have a property for each field in the data model."""
        assert_has_a_property_for_each_data_field(PhotoModel, PhotoData)

    fields_name_initial_new = [
        ("original_filename", Path("img_001.jpg"), Path("img_002.jpg")),
        ("width", 1024, 2048),
        ("height", 768, 1536),
        ("quadrat_corners", None, [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]),
        ("camera_matrix", None, ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, 1.0))),
        ("distortion_coefficients", None, [0.01, -0.02, 0.0, 0.0]),
        ("red_shift", None, (0.3, -0.2)),
        ("blue_shift", None, (0.0, 0.5)),
    ]

    @pytest.mark.parametrize("field_name, initial_value, new_value", fields_name_initial_new)
    def test_properties_getter_setter_and_signals(
        self, qtbot: QtBot, field_name: str, initial_value: object, new_value: object
    ) -> None:
        """Model properties should have working getters, setters, and change signals."""
        # Arrange: empty MetadataModel
        model = self.create_test_model()

        # Assert: fields signal correctly on change
        assert_model_property_getter_setter_and_signal(qtbot, model, field_name, initial_value, new_value)

    fields_name_invalid = [
        # Invalid type
        ("width", "not an int"),  # Invalid type
        ("height", "not an int"),  # Invalid type
        ("width", 1024.5),  # Invalid type
        ("height", 768.5),  # Invalid type
        ("quadrat_corners", "not a list"),  # Invalid type
        ("camera_matrix", "not a matrix"),  # Invalid type
        ("distortion_coefficients", "not a list"),  # Invalid type
        ("red_shift", "not a tuple"),  # Invalid type
        ("blue_shift", "not a tuple"),  # Invalid type
        # Too many values
        ("width", -10),  # Negative width
        ("height", -10),  # Negative height
        ("width", 0),  # Zero width
        ("height", 0),  # Zero height
        ("quadrat_corners", [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (2.0, 2.0)]),  # Too many corners
        ("camera_matrix", ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0))),  # Not 3x3
        ("distortion_coefficients", [0.01, -0.02]),  # Too few coefficients
        ("red_shift", (0.3, -0.2, 0.1)),  # Too many values
        ("blue_shift", (0.0, 0.5, 0.1)),  # Too many values
    ]

    @pytest.mark.parametrize("field_name, invalid_value", fields_name_invalid)
    def test_properties_validation(self, field_name: str, invalid_value: object) -> None:
        """Model properties should enforce type validation and constraints when set."""
        model = self.create_test_model()

        with pytest.raises(ValueError):
            setattr(model, field_name, invalid_value)

    fields_name_value_normalized = [
        # Paths are normalized
        ("original_filename", "img_003.jpg", Path("img_003.jpg")),  # str to Path
        # Empty lists become None
        ("quadrat_corners", [], None),
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
        model = self.create_test_model()

        # Assert: metadata is accessible
        assert model.metadata is not None

        initial_partner_value = model.metadata.partner

        assert_model_property_signals_on_mutation(
            qtbot,
            model,
            "metadata",
            fn_set_same=lambda m, p: setattr(m.metadata, "partner", initial_partner_value),
            fn_set_new=lambda m, p: setattr(m.metadata, "partner", "Acme Corp"),
        )

    def test_serialize_deserialize(self) -> None:
        # Arrange
        photo0 = PhotoModel(
            PhotoData(
                original_filename=Path("img_001.jpg"),
                width=1024,
                height=768,
            )
        )

        # Assert: defaults set (quadrat_corners defaults to None)
        assert photo0.original_filename == Path("img_001.jpg")
        assert photo0.quadrat_corners is None
        assert photo0.red_shift is None
        assert photo0.blue_shift is None

        # Act: Serialize and deserialize
        json_str0: str = photo0._data.model_dump_json()
        photo1: PhotoModel = PhotoModel(PhotoData.model_validate_json(json_str0))

        # Assert: values read
        assert photo1.original_filename == photo0.original_filename
        assert photo1.quadrat_corners == photo0.quadrat_corners
        assert photo1.red_shift == photo0.red_shift
        assert photo1.blue_shift == photo0.blue_shift
        assert photo1.camera_matrix == photo0.camera_matrix
        assert photo1.distortion_coefficients == photo0.distortion_coefficients

        # Act: Set some values
        corners = [(0.1, 0.2), (1.1, 0.2), (1.1, 1.2), (0.1, 1.2)]
        camera = (
            (1000.0, 0.0, 512.0),
            (0.0, 1000.0, 384.0),
            (0.0, 0.0, 1.0),
        )
        distortion = [0.01, -0.02, 0.0, 0.0]
        photo1.original_filename = Path("img_001.jpg")
        photo1.quadrat_corners = corners
        photo1.red_shift = (0.3, -0.2)
        photo1.blue_shift = (0.0, 0.5)
        photo1.camera_matrix = camera
        photo1.distortion_coefficients = distortion

        # Assert: verify values set
        assert photo1.original_filename == Path("img_001.jpg")
        assert photo1.quadrat_corners == corners
        assert photo1.red_shift == (0.3, -0.2)
        assert photo1.blue_shift == (0.0, 0.5)
        assert photo1.camera_matrix == camera
        assert photo1.distortion_coefficients == distortion

        # Act: Serialize and deserialize
        json_str1: str = photo1._data.model_dump_json()
        photo2: PhotoModel = PhotoModel(PhotoData.model_validate_json(json_str1))

        # Assert: verify values read
        assert photo2.original_filename == Path("img_001.jpg")
        assert photo2.quadrat_corners == corners
        assert photo2.red_shift == (0.3, -0.2)
        assert photo2.blue_shift == (0.0, 0.5)
        assert photo2.camera_matrix == camera
        assert photo2.distortion_coefficients == distortion
