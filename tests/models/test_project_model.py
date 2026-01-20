import unittest


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

    def test_serialize_deserialize_photos(self) -> None:
        # Arrange
        project = ProjectModel()
        p = PhotoModel()
        p.original_filename = "picA.jpg"
        p.red_shift = (1.0, 2.0)
        project.photos.append(p)

        # Act: serialize
        s = project.serialize()

        # Assert serialized structure
        self.assertIn("photos", s)
        self.assertIsInstance(s["photos"], list)
        self.assertEqual(len(s["photos"]), 1)
        self.assertEqual(s["photos"][0]["original_filename"], "picA.jpg")
        self.assertEqual(s["photos"][0]["red_shift"], [1.0, 2.0])

        # Arrange a fresh project to deserialize into and watch for on_changed
        new_project = ProjectModel()
        changed = False

        def handle_changed() -> None:
            nonlocal changed
            changed = True

        new_project.on_changed.connect(handle_changed)

        # Act: deserialize
        new_project.deserialize(s)

        # Assert: one photo restored with properties
        self.assertEqual(len(new_project.photos), 1)
        restored = new_project.photos[0]
        self.assertIsInstance(restored, PhotoModel)
        self.assertEqual(restored.original_filename, "picA.jpg")
        self.assertEqual(restored.red_shift, (1.0, 2.0))
        self.assertTrue(changed)

        # Act: clear photos via deserialize with None
        changed = False
        new_project.deserialize({"photos": None})

        # Assert: photos cleared and on_changed emitted
        self.assertEqual(len(new_project.photos), 0)
        self.assertTrue(changed)
