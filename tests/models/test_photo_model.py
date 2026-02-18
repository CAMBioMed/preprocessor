import unittest
from PySide6.QtCore import Slot

from preprocessor.model.photo_model import PhotoModel, PhotoData


class TestPhotoModel(unittest.TestCase):
    def test_quadrat_corners(self) -> None:
        # Arrange
        photo = PhotoModel()

        raised_quadrat_corners_changed = False
        raised_changed = False

        @Slot()
        def handle_quadrat() -> None:
            nonlocal raised_quadrat_corners_changed
            raised_quadrat_corners_changed = True

        @Slot()
        def handle_changed() -> None:
            nonlocal raised_changed
            raised_changed = True

        photo.on_quadrat_corners_changed.connect(handle_quadrat)
        photo.on_changed.connect(handle_changed)

        # Assert initial state
        assert photo.quadrat_corners == []
        assert not raised_quadrat_corners_changed
        assert not raised_changed

        # Act: set quadrat corners
        corners = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        photo.quadrat_corners = corners

        # Assert: property set and both signals fired
        assert photo.quadrat_corners == corners
        assert raised_quadrat_corners_changed
        assert raised_changed

        # Act: set same value again -> no signals
        raised_quadrat_corners_changed = False
        raised_changed = False
        photo.quadrat_corners = corners

        # Assert: no signals fired when value unchanged
        assert not raised_quadrat_corners_changed
        assert not raised_changed

        # Act: clear the value
        photo.quadrat_corners = []

        # Assert: property cleared and signals fired
        assert photo.quadrat_corners == []
        assert raised_quadrat_corners_changed
        assert raised_changed

    def test_serialize_deserialize(self) -> None:
        # Arrange
        photo = PhotoModel()

        # Act: Serialize using defaults
        s_none = photo.serialize()

        # Assert
        assert "original_filename" in s_none
        assert s_none["original_filename"] is None
        assert "quadrat_corners" in s_none
        assert s_none["quadrat_corners"] == []
        assert "red_shift" in s_none
        assert "blue_shift" in s_none
        assert s_none["red_shift"] is None
        assert s_none["blue_shift"] is None
        assert "camera_matrix" in s_none
        assert "distortion_coefficients" in s_none
        assert s_none["camera_matrix"] is None
        assert s_none["distortion_coefficients"] is None

        # Act: Set corners and serialize
        corners = [(0.1, 0.2), (1.1, 0.2), (1.1, 1.2), (0.1, 1.2)]
        photo.quadrat_corners = corners
        photo.red_shift = (0.3, -0.2)
        photo.blue_shift = (0.0, 0.5)
        photo.original_filename = "img_001.jpg"
        camera = (
            (1000.0, 0.0, 512.0),
            (0.0, 1000.0, 384.0),
            (0.0, 0.0, 1.0),
        )
        distortion = ((0.01, -0.02), (0.0, 0.0))
        photo.camera_matrix = camera
        photo.distortion_coefficients = distortion
        s = photo.serialize()

        # Assert
        assert s == {
            "original_filename": "img_001.jpg",
            "quadrat_corners": [(0.1, 0.2), (1.1, 0.2), (1.1, 1.2), (0.1, 1.2)],
            "red_shift": (0.3, -0.2),
            "blue_shift": (0.0, 0.5),
            "camera_matrix": ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, 1.0)),
            "distortion_coefficients": ((0.01, -0.02), (0.0, 0.0)),
        }

        # Arrange: Deserialize into a fresh model and verify signals and value
        new_photo = PhotoModel()
        raised_quadrat = False
        raised_quadrat_corners_changed = False
        raised_red = False
        raised_blue = False
        raised_camera = False
        raised_distortion = False
        raised_changed = False
        raised_original = False

        @Slot()
        def handle_quadrat() -> None:
            nonlocal raised_quadrat
            raised_quadrat = True

        @Slot()
        def handle_changed() -> None:
            nonlocal raised_quadrat_corners_changed
            nonlocal raised_red, raised_blue, raised_camera
            nonlocal raised_distortion, raised_changed
            raised_quadrat_corners_changed = True
            raised_changed = True

        new_photo.on_quadrat_corners_changed.connect(handle_quadrat)
        new_photo.on_changed.connect(handle_changed)

        @Slot()
        def handle_red() -> None:
            nonlocal raised_red
            raised_red = True

        @Slot()
        def handle_blue() -> None:
            nonlocal raised_blue
            raised_blue = True

        @Slot()
        def handle_camera() -> None:
            nonlocal raised_camera
            raised_camera = True

        @Slot()
        def handle_distortion() -> None:
            nonlocal raised_distortion
            raised_distortion = True

        @Slot()
        def handle_original() -> None:
            nonlocal raised_original
            raised_original = True

        new_photo.on_red_shift_changed.connect(handle_red)
        new_photo.on_blue_shift_changed.connect(handle_blue)
        new_photo.on_camera_matrix_changed.connect(handle_camera)
        new_photo.on_distortion_coefficients_changed.connect(handle_distortion)
        new_photo.on_original_filename_changed.connect(handle_original)

        # Act
        new_photo.deserialize(s)

        # Assert
        assert str(new_photo.original_filename) == "img_001.jpg"
        assert new_photo.quadrat_corners == corners
        assert new_photo.red_shift == (0.3, -0.2)
        assert new_photo.blue_shift == (0.0, 0.5)
        assert new_photo.camera_matrix == camera
        assert new_photo.distortion_coefficients == distortion
        assert raised_original
        assert raised_quadrat
        assert raised_quadrat_corners_changed
        assert raised_red
        assert raised_blue
        assert raised_camera
        assert raised_distortion
        assert raised_changed

        # Act: Deserialize None to clear
        raised_quadrat = False
        raised_quadrat_corners_changed = False
        raised_red = False
        raised_blue = False
        raised_camera = False
        raised_distortion = False
        raised_changed = False
        raised_original = False
        new_photo.deserialize(
            {
                "original_filename": None,
                "quadrat_corners": [],
                "red_shift": None,
                "blue_shift": None,
                "camera_matrix": None,
                "distortion_coefficients": None,
            }
        )

        # Assert
        assert new_photo.original_filename is None
        assert new_photo.quadrat_corners == []
        assert new_photo.camera_matrix is None
        assert new_photo.distortion_coefficients is None
        assert raised_original
        assert raised_quadrat
        assert raised_quadrat_corners_changed
        assert raised_red
        assert raised_blue
        assert raised_camera
        assert raised_distortion
        assert raised_changed
