import unittest
from PySide6.QtCore import Slot

from preprocessor.model.photo_model import PhotoModel


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
        self.assertIsNone(photo.quadrat_corners)
        self.assertFalse(raised_quadrat_corners_changed)
        self.assertFalse(raised_changed)

        # Act: set quadrat corners
        corners = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))
        photo.quadrat_corners = corners

        # Assert: property set and both signals fired
        self.assertEqual(photo.quadrat_corners, corners)
        self.assertTrue(raised_quadrat_corners_changed)
        self.assertTrue(raised_changed)

        # Act: set same value again -> no signals
        raised_quadrat_corners_changed = False
        raised_changed = False
        photo.quadrat_corners = corners

        # Assert: no signals fired when value unchanged
        self.assertFalse(raised_quadrat_corners_changed)
        self.assertFalse(raised_changed)

        # Act: clear the value
        photo.quadrat_corners = None

        # Assert: property cleared and signals fired
        self.assertIsNone(photo.quadrat_corners)
        self.assertTrue(raised_quadrat_corners_changed)
        self.assertTrue(raised_changed)

    def test_serialize_deserialize(self) -> None:
        # Arrange
        photo = PhotoModel()

        # Act: Serialize using defaults
        s_none = photo.serialize()

        # Assert
        self.assertIn("quadrat_corners", s_none)
        self.assertIsNone(s_none["quadrat_corners"])
        self.assertIn("red_shift", s_none)
        self.assertIn("blue_shift", s_none)
        self.assertIsNone(s_none["red_shift"])
        self.assertIsNone(s_none["blue_shift"])

        # Act: Set corners and serialize
        corners = ((0.1, 0.2), (1.1, 0.2), (1.1, 1.2), (0.1, 1.2))
        photo.quadrat_corners = corners
        photo.red_shift = (0.3, -0.2)
        photo.blue_shift = (0.0, 0.5)
        s = photo.serialize()

        # Assert
        self.assertEqual(s, {
            "quadrat_corners": [[0.1, 0.2], [1.1, 0.2], [1.1, 1.2], [0.1, 1.2]],
            "red_shift": [0.3, -0.2],
            "blue_shift": [0.0, 0.5],
        })

        # Arrange: Deserialize into a fresh model and verify signals and value
        new_photo = PhotoModel()
        raised_quadrat = False
        raised_quadrat_corners_changed = False
        raised_red = False
        raised_blue = False
        raised_changed = False

        @Slot()
        def handle_quadrat() -> None:
            nonlocal raised_quadrat
            raised_quadrat = True

        @Slot()
        def handle_changed() -> None:
            nonlocal raised_quadrat_corners_changed, raised_red, raised_blue, raised_changed
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

        new_photo.on_red_shift_changed.connect(handle_red)
        new_photo.on_blue_shift_changed.connect(handle_blue)

        # Act
        new_photo.deserialize(s)

        # Assert
        self.assertEqual(new_photo.quadrat_corners, corners)
        self.assertEqual(new_photo.red_shift, (0.3, -0.2))
        self.assertEqual(new_photo.blue_shift, (0.0, 0.5))
        self.assertTrue(raised_quadrat)
        self.assertTrue(raised_quadrat_corners_changed)
        self.assertTrue(raised_red)
        self.assertTrue(raised_blue)
        self.assertTrue(raised_changed)

        # Act: Deserialize None to clear
        raised_quadrat = False
        raised_quadrat_corners_changed = False
        raised_red = False
        raised_blue = False
        raised_changed = False
        new_photo.deserialize({"quadrat_corners": None, "red_shift": None, "blue_shift": None})

        # Assert
        self.assertIsNone(new_photo.quadrat_corners)
        self.assertTrue(raised_quadrat)
        self.assertTrue(raised_quadrat_corners_changed)
        self.assertTrue(raised_red)
        self.assertTrue(raised_blue)
        self.assertTrue(raised_changed)
