import unittest

from PySide6.QtCore import Slot

from preprocessor.model.project_model import ProjectModel
from preprocessor.model.photo_model import PhotoModel
from preprocessor.model.list_model import QListModel



class TestProjectModel(unittest.TestCase):
    def test_photos(self) -> None:
        # Arrange
        project_model = ProjectModel()

        # Assert initial state
        self.assertIsInstance(project_model.photos, QListModel)
        self.assertEqual(project_model.photos.parent(), project_model)

        # Act: add a photo
        photo0 = PhotoModel()
        self.assertEqual(photo0.parent(), None)

        project_model.photos.append(photo0)

        # Assert: photo added and parent set to photos list
        self.assertIs(project_model.photos[0], photo0)
        self.assertEqual(photo0.parent(), project_model.photos)

        # Act: remove the photo
        project_model.photos.remove(photo0)

        # Assert: removed and parent cleared
        self.assertEqual(len(project_model.photos), 0)
        self.assertEqual(photo0.parent(), None)
