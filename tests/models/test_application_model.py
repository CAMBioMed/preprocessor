from pathlib import Path

import pytest
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication

from preprocessor.model.application_model import ApplicationModel
from preprocessor.model.project_model import ProjectModel

# Ensure a Qt application context exists for QObject usage in tests. Rely on pytest-qt's qapp.
@pytest.fixture(autouse=True)
def _ensure_qapp(qapp: QApplication) -> QApplication:
    return qapp

class TestApplicationModel:
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

        project_model0 = ProjectModel(file=Path("test_project0.json"))

        # Assert
        assert project_model0.parent() is None
        assert not raised_on_changed
        assert raised_on_current_project_changed is None

        # Act: Set current_project to project_model0
        raised_on_changed = False
        app_model.current_project = project_model0

        # Assert
        assert app_model.current_project == project_model0
        assert project_model0.parent() == app_model
        assert raised_on_changed
        assert raised_on_current_project_changed == project_model0

        # Act: Set current_project to project_model1
        raised_on_changed = False
        project_model1 = ProjectModel(file=Path("test_project1.json"))
        app_model.current_project = project_model1

        # Assert
        assert app_model.current_project == project_model1
        assert project_model1.parent() == app_model
        assert project_model0.parent() is None
        assert raised_on_changed
        assert raised_on_current_project_changed == project_model1
