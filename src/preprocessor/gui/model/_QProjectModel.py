import contextlib
import logging
from pathlib import Path
from typing import Any

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QFileDialog, QApplication, QMessageBox

from preprocessor.core.model import ProjectData
from preprocessor.gui.model._QPhotoModel import QPhotoModel
from preprocessor.gui.model._QListModel import QListModel
from preprocessor.gui.model._QModel import QModel

logger = logging.getLogger(__name__)

class QProjectModel(QModel[ProjectData]):
    """The model for a project, used for the GUI."""

    on_project_file_changed: Signal = Signal(Path)
    on_photos_changed: Signal = Signal()
    on_photos_path_changed: Signal = Signal(object)  # Emits Path | None
    on_export_path_changed: Signal = Signal(object)  # Emits Path | None

    _photos: QListModel[QPhotoModel]
    _connected_photos: set[QPhotoModel]

    def __init__(self, data: ProjectData | dict[str, Any] | None = None) -> None:
        super().__init__(model_cls=ProjectData, data=data)

        # Create QListModel containers for interactive use
        self._photos = QListModel[QPhotoModel](parent=self)
        # Track which model instances we've connected signal handlers to
        self._connected_photos: set[QPhotoModel] = set()
        # Wire photos list changes to mark dirty and (re)wire photo handlers
        self._photos.bind_to_model(self, "photos", self._handle_photos_changed)
        # Populate the QListModel containers from the initial data
        self._photos.populate_from_data(self._data.photos, QPhotoModel)

    ################
    ## Properties ##
    ################

    @property
    def project_file(self) -> Path | None:
        """The file path where the project is or will be saved, or None if not set.
        This property is not serialized/deserialized.
        """
        return self._data.project_file

    @project_file.setter
    def project_file(self, path: Path | None) -> None:
        self._set_field("project_file", path)

    @property
    def photos(self) -> QListModel[QPhotoModel]:
        """The list of photos in the project."""
        return self._photos

    @property
    def photos_path(self) -> Path | None:
        """The file path from which photos were last added, or None if not set."""
        return self._data.photos_path

    @photos_path.setter
    def photos_path(self, path: Path | None) -> None:
        self._set_field("photos_path", path)

    @property
    def export_path(self) -> Path | None:
        """The file path where the photos will be exported to, or None if not set."""
        return self._data.export_path

    @export_path.setter
    def export_path(self, path: Path | None) -> None:
        self._set_field("export_path", path)

    #####################
    ## Signal Handlers ##
    #####################

    def _handle_photos_changed(self) -> None:
        """Handle a change in the photo models."""
        self.mark_dirty()
        with contextlib.suppress(Exception):
            self.on_photos_changed.emit()
        with contextlib.suppress(Exception):
            self.on_changed.emit()

    @staticmethod
    def new_project(
        parent: QWidget | None,
        old_project: "QProjectModel | None",
        initial_dir: Path | None,
    ) -> "QProjectModel | None":
        """
        Return the new QProjectModel if successful, or None if canceled or failed.

        If `old_project` is not None and there are unsaved changes, the user will be prompted to save
        before creating a new project; if they choose to cancel, this function will return None.

        :param parent: The parent widget for the dialog.
        :param old_project: The existing project model that may have unsaved changes; can be None if no project is open.
        :param initial_dir: An optional initial directory for the save dialog; can be None to use the default.
        :return: A new QProjectModel if a project was created, or None if the operation was canceled or failed.
        """
        if not QProjectModel.save_project_if_dirty(parent, old_project, initial_dir):
            return None
        return QProjectModel(ProjectData())

    @staticmethod
    def open_project(
        parent: QWidget | None,
        old_project: "QProjectModel | None",
        initial_dir: Path | None,
    ) -> "QProjectModel | None":
        """
        Show a file dialog to open a project file, and return the loaded QProjectModel if successful,
        or None if canceled or failed.

        If `old_project` is not None and there are unsaved changes, the user will be prompted to save
        before opening a new project; if they choose to cancel, this function will return None.

        :param parent: The parent widget for the dialog.
        :param old_project: The existing project model that may have unsaved changes; can be None if no project is open.
        :param initial_dir: An optional initial directory to open the file dialog in; can be None to use the default.
        :return: A loaded QProjectModel if a project was opened, or None if the operation was canceled or failed.
        """
        path, _ = QFileDialog.getOpenFileName(
            parent,
            "Open Project",
            str(initial_dir) if initial_dir else "",
            "Project Files (*.pbproj);;All Files (*)",
        )
        if not path:
            return None
        return QProjectModel.open_project_from_path(parent, old_project, Path(path), initial_dir)

    @staticmethod
    def save_project(
        parent: QWidget | None,
        project: "QProjectModel",
        initial_dir: Path | None,
    ) -> bool:
        """
        Save the given project; return True if successful, False if canceled or failed.

        :param parent: The parent widget for any dialogs; can be None if not needed.
        :param project: The project model to save; must not be None.
        :param initial_dir: An optional initial directory to open the file save dialog in; can be None to use the default.
        :return: True if the project was successfully saved, or False if the operation was canceled or failed.
        """
        if project.project_file is not None:
            return QProjectModel.save_project_to_path(parent, project, project.project_file)
        return QProjectModel.save_project_as(parent, project, initial_dir)

    @staticmethod
    def save_project_as(
        parent: QWidget | None,
        project: "QProjectModel",
        initial_dir: Path | None,
    ) -> bool:
        """
        Show a file dialog to save the given project.

        :param parent: The parent widget for the dialog.
        :param project: The project model to save; must not be None.
        :param initial_dir: An optional initial directory to open the file dialog in; can be None to use the default.
        :return: True if the project was successfully saved, or False if the operation was canceled or failed.
.       """
        path, _ = QFileDialog.getSaveFileName(
            parent,
            "Save Project",
            str(project.project_file) if project.project_file else str(initial_dir) if initial_dir else "",
            "Project Files (*.pbproj);;All Files (*)",
        )
        if not path:
            return False
        return QProjectModel.save_project_to_path(parent, project, Path(path))

    @staticmethod
    def save_project_if_dirty(
        parent: QWidget | None,
        project: "QProjectModel | None",
        initial_dir: Path | None,
    ) -> bool:
        """
        If the project has unsaved changes, prompt the user to save; return True if it's now safe to proceed
        (either no unsaved changes or the user saved or chose not to save), or False if the user canceled.

        :param parent: The parent widget for the dialog.
        :param project: The project model that may have unsaved changes; can be None if no project is open.
        :return: True if it's safe to proceed (no unsaved changes, or the user saved, or the user chose not to save),
        or False if the user canceled.
        """
        if project is None or not project.dirty:
            return True
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Unsaved Changes")
        msg_box.setText("The current project has unsaved changes. Do you want to save before proceeding?")
        save_button = msg_box.addButton("Save", QMessageBox.ButtonRole.AcceptRole)
        discard_button = msg_box.addButton("Discard", QMessageBox.ButtonRole.DestructiveRole)
        msg_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        msg_box.exec()

        clicked_button = msg_box.clickedButton()
        if clicked_button == save_button:
            return QProjectModel.save_project(parent, project, initial_dir)
        return clicked_button == discard_button

    @staticmethod
    def open_project_from_path(
        parent: QWidget | None,
        old_project: "QProjectModel | None",
        new_project_file: Path,
        initial_dir: Path | None,
    ) -> "QProjectModel | None":
        """
        Show a file dialog to open a project file, and return the loaded QProjectModel if successful,
        or None if canceled or failed.

        If `old_project` is not None and there are unsaved changes, the user will be prompted to save
        before opening a new project; if they choose to cancel, this function will return None.

        :param parent: The parent widget for the dialog.
        :param old_project: The existing project model that may have unsaved changes; can be None if no project is open.
        :param new_project_file: The file path to the project file to open.
        :param initial_dir: An optional initial directory to open the file save dialog in; can be None to use the default.
        :return: A loaded QProjectModel if a project was opened, or None if the operation was canceled or failed.
        """
        if not QProjectModel.save_project_if_dirty(parent, old_project, initial_dir):
            return None
        try:
            project_data = ProjectData.load_from_file(new_project_file)
            project_model = QProjectModel(project_data)
            project_model.project_file = new_project_file
            project_model.mark_clean()
            return project_model
        except FileNotFoundError as exc:
            logger.exception("Project file not found: %s", new_project_file, exc_info=exc)
            if QApplication.instance() is not None:
                QMessageBox.critical(
                    parent,
                    "Open Project Failed",
                    f"Project file not found:\n{new_project_file}\n\n{exc}",
                )
            return None
        except ValueError as exc:
            logger.exception("Failed to open project file %s: %s", new_project_file, exc_info=exc)
            if QApplication.instance() is not None:
                QMessageBox.critical(
                    parent,
                    "Open Project Failed",
                    f"Project file appears invalid:\n{new_project_file}\n\n{exc}",
                )
            return None

    @staticmethod
    def save_project_to_path(
        parent: QWidget | None,
        project_model: "QProjectModel",
        path: Path,
    ) -> bool:
        """
        Save the given project to the given path; return True if successful, False if canceled or failed.

        :param parent: The parent widget for any dialogs; can be None if not needed.
        :param project_model: The project model to save; must not be None.
        :param path: The file path to save the project to.
        :return: True if the project was successfully saved, or False if the operation failed.
        """
        try:
            project_data = project_model._data
            project_data.save_to_file(path)
            project_model.project_file = path
            project_model.mark_clean()
        except Exception as exc:
            logger.exception("Failed to save project file %s: %s", path, exc)
            if QApplication.instance() is not None:
                QMessageBox.critical(
                    parent,
                    "Save Project Failed",
                    f"Failed to save project file:\n{path}\n\n{exc}",
                )
            return False
        return True
