from pathlib import Path
from typing import cast

from PySide6.QtCore import QObject, Signal, QSettings, QByteArray

from preprocessor.model.photo_model import PhotoModel
from preprocessor.model.project_model import ProjectModel


class ApplicationModel(QObject):
    """
    The model for the entire application.

    This includes application-wide settings and the current project.
    """

    on_changed: Signal = Signal()

    settings: QSettings

    def __init__(self) -> None:
        super().__init__()
        self.settings = QSettings()

    _current_project: ProjectModel = ProjectModel(file=Path("empty"))  # placeholder empty project model
    on_current_project_changed: Signal = Signal(object)  # https://stackoverflow.com/a/57810835/146622

    @property
    def current_project(self) -> ProjectModel:
        """The current project model, or None if no project is open."""
        return self._current_project

    @current_project.setter
    def current_project(self, project: ProjectModel) -> None:
        old_project = self._current_project
        if old_project != project:
            old_project.setParent(None)
            self._current_project = project
            project.setParent(self)
            self.on_current_project_changed.emit(project)
            self.on_changed.emit()

    _current_photo: PhotoModel | None = None
    on_current_photo_changed: Signal = Signal(object)  # https://stackoverflow.com/a/57810835/146622

    @property
    def current_photo(self) -> PhotoModel | None:
        """The current project model, or None if no project is open."""
        return self._current_photo

    @current_photo.setter
    def current_photo(self, photo: PhotoModel | None) -> None:
        old_photo = self._current_photo
        if old_photo != photo:
            self._current_photo = photo
            self.on_current_photo_changed.emit(photo)
            self.on_changed.emit()

    _main_window_geometry: QByteArray = QByteArray()

    @property
    def main_window_geometry(self) -> QByteArray:
        """The geometry of the main window."""
        return self._main_window_geometry

    @main_window_geometry.setter
    def main_window_geometry(self, geometry: QByteArray) -> None:
        self._main_window_geometry = geometry

    _main_window_state: QByteArray = QByteArray()

    @property
    def main_window_state(self) -> QByteArray:
        """The state of the main window."""
        return self._main_window_state

    @main_window_state.setter
    def main_window_state(self, state: QByteArray) -> None:
        self._main_window_state = state

    def write_settings(self) -> None:
        """Write window settings to persistent storage."""
        self.settings.setValue("geometry", self._main_window_geometry)
        self.settings.setValue("windowState", self._main_window_state)

    def read_settings(self) -> None:
        """Read window settings from persistent storage."""
        self._main_window_geometry = cast(QByteArray, self.settings.value("geometry", QByteArray()))
        self._main_window_state = cast(QByteArray, self.settings.value("windowState", QByteArray()))
