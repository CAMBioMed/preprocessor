import contextlib
from pathlib import Path
from typing import Any

from PySide6.QtCore import Signal

from preprocessor.core.model import ProjectData, MetadataData, ColorCorrectionParams, LensCorrectionParams, CropParams
from preprocessor.gui.model import QPhotoModel
from preprocessor.model.qlistmodel import QListModel
from preprocessor.model.qmodel import QModel


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
