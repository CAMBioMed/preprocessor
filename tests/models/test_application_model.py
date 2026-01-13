import unittest

from PySide6.QtCore import Slot

from preprocessor.model.model import ApplicationModel
from preprocessor.model.model import ProjectModel



class TestApplicationModel(unittest.TestCase):
    def test_current_project(self) -> None:
        # Arrange
        app_model = ApplicationModel()

        raised_on_changed = False
        @Slot()
        def handle_on_changed() -> None:
            nonlocal raised_on_changed
            raised_on_changed = True
        app_model.on_changed.connect(handle_on_changed)

        raised_on_current_project_changed = None
        @Slot(object)
        def handle_on_current_project_changed(project: ProjectModel) -> None:
            nonlocal raised_on_current_project_changed
            raised_on_current_project_changed = project
        app_model.on_current_project_changed.connect(handle_on_current_project_changed)

        project_model0 = ProjectModel()

        # Assert
        self.assertEqual(app_model.current_project, None)
        self.assertEqual(project_model0.parent(), None)
        self.assertEqual(raised_on_changed, False)
        self.assertEqual(raised_on_current_project_changed, None)

        # Act: Set current_project to project_model0
        raised_on_changed = False
        app_model.current_project = project_model0

        # Assert
        self.assertEqual(app_model.current_project, project_model0)
        self.assertEqual(project_model0.parent(), app_model)
        self.assertEqual(raised_on_changed, True)
        self.assertEqual(raised_on_current_project_changed, project_model0)

        # Act: Set current_project to project_model1
        raised_on_changed = False
        project_model1 = ProjectModel()
        app_model.current_project = project_model1

        # Assert
        self.assertEqual(app_model.current_project, project_model1)
        self.assertEqual(project_model1.parent(), app_model)
        self.assertEqual(project_model0.parent(), None)
        self.assertEqual(raised_on_changed, True)
        self.assertEqual(raised_on_current_project_changed, project_model1)

        # Act: Set current_project to None
        raised_on_changed = False
        app_model.current_project = None

        # Assert
        self.assertEqual(app_model.current_project, None)
        self.assertEqual(project_model1.parent(), None)
        self.assertEqual(project_model0.parent(), None)
        self.assertEqual(raised_on_changed, True)
        self.assertEqual(raised_on_current_project_changed, None)