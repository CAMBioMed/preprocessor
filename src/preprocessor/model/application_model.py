from PySide6.QtCore import QObject, Signal

from preprocessor.model.project_model import ProjectModel


class ApplicationModel(QObject):
    """
    The model for the entire application.

    This includes application-wide settings and the current project.
    """

    on_changed: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

    _current_project: ProjectModel | None = None
    on_current_project_changed: Signal = Signal(object)  # https://stackoverflow.com/a/57810835/146622

    @property
    def current_project(self) -> ProjectModel | None:
        """The current project model, or None if no project is open."""
        return self._current_project

    @current_project.setter
    def current_project(self, project: ProjectModel | None) -> None:
        old_project = self._current_project
        if old_project != project:
            if old_project is not None:
                old_project.setParent(None)
            self._current_project = project
            if project is not None:
                project.setParent(self)
            self.on_current_project_changed.emit(project)
            self.on_changed.emit()


