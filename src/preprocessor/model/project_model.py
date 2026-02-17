from PySide6.QtCore import QObject, Signal
from pydantic import BaseModel, Field

from preprocessor.model.camera_model import CameraModel, CameraData
from preprocessor.model.qlistmodel import QListModel
from preprocessor.model.photo_model import PhotoModel, PhotoData

# Add imports for file IO
import json
from pathlib import Path
from typing import Union, Set, Iterable, ClassVar, Any

from preprocessor.model.qmodel import QModel


class ProjectData(BaseModel):
    """
    The data for a project, including project-specific settings.
    """

    # Serialization JSON version
    SERIAL_VERSION: ClassVar[int] = 1

    file: Path | None = Field(default=None, exclude=True)
    """The file path of the project file, or None if not saved yet. This is not serialized/deserialized."""
    export_path: Path | None = None
    """The file path where the photos will be exported to, or None if not set."""
    target_width: int | None = None
    """The target width for perspective correction, or None if not set."""
    target_height: int | None = None
    """The target height for perspective correction, or None if not set."""
    photos: list[PhotoData] = []
    """The list of photos in the project."""
    cameras: list[CameraData] = []
    """The list of cameras in the project."""



class ProjectModel(QModel[ProjectData]):

    on_file_changed: Signal = Signal(object)
    on_export_path_changed: Signal = Signal(object)
    on_target_width_changed: Signal = Signal(object)
    on_target_height_changed: Signal = Signal(object)

    _photos: QListModel[PhotoModel]
    _cameras: QListModel[CameraModel]

    def __init__(self, data: ProjectData | dict[str, Any] | None = None) -> None:
        super().__init__(model_cls=ProjectData, data=data)

        # Create QListModel containers for interactive use
        self._photos = QListModel[PhotoModel](parent = self)
        self._cameras = QListModel[CameraModel](parent = self)

        # Track which model instances we've connected to
        self._connected_photos: Set[PhotoModel] = set()
        self._connected_cameras: Set[CameraModel] = set()

        # wire photos list changes to mark dirty and (re)wire photo handlers
        self._photos.bind_to_model(self, "photos", self._handle_child_changed)
        self._cameras.bind_to_model(self, "cameras", self._handle_child_changed)

        self._populate_lists_from_data()

    @property
    def file(self) -> Path | None:
        """
        The file path where the project is saved, or None if not saved yet.

        This property is not serialized/deserialized.
        """
        return self._data.file

    @file.setter
    def file(self, path: Path | None) -> None:
        self._set_field("file", path)


    @property
    def export_path(self) -> Path | None:
        """
        The file path where the photos will be exported to, or None if not set.
        """
        return self._data.export_path

    @export_path.setter
    def export_path(self, path: Path | None) -> None:
        self._set_field("export_path", path)


    @property
    def target_width(self) -> int | None:
        """The target width for perspective correction, or None if not set."""
        return self._data.target_width

    @target_width.setter
    def target_width(self, value: int | None) -> None:
        self._set_field("target_width", value)


    @property
    def target_height(self) -> int | None:
        """The target height for perspective correction, or None if not set."""
        return self._data.target_height

    @target_height.setter
    def target_height(self, value: int | None) -> None:
        self._set_field("target_height", value)


    @property
    def photos(self) -> QListModel[PhotoModel]:
        """The list of photos in the project."""
        return self._photos

    @property
    def cameras(self) -> QListModel[CameraModel]:
        """The list of cameras in the project."""
        return self._cameras

    # ----- sync helpers -----
    # def _populate_lists_from_data(self) -> None:
    #     """
    #     Populate the QListModels from the current self._data (ProjectData).
    #     Called at init and after deserialize().
    #     """
    #     # populate photos
    #     for item in list(self._photos):
    #         self._photos.remove(item)
    #     if self._data.photos:
    #         for pdata in self._data.photos:
    #             pm = PhotoModel(data=pdata)
    #             self._photos.append(pm)
    #
    #     # populate cameras
    #     for item in list(self._cameras):
    #         self._cameras.remove(item)
    #     if self._data.cameras:
    #         for cdata in self._data.cameras:
    #             cm = CameraModel(data=cdata)
    #             self._cameras.append(cm)

    def _populate_lists_from_data(self) -> None:
        """
        Populate the QListModels from the current self._data (ProjectData).
        Uses the QListModel helper to reduce boilerplate.
        """
        self._photos.populate_from_data(self._data.photos, PhotoModel)
        self._cameras.populate_from_data(self._data.cameras, CameraModel)

    def _handle_child_changed(self) -> None:
        """Called when any child model reports a change."""
        self.mark_dirty()
        try:
            self.on_changed.emit()
        except Exception:
            pass
    # # internal handlers for wiring child signals
    # def _handle_photos_changed(self, added: Iterable[PhotoModel], removed: Iterable[PhotoModel]) -> None:
    #     """
    #     Called when the photos QListModel changes.
    #     Marks project dirty and (re)wires per-photo on_changed handlers.
    #     """
    #     # any modification to the list counts as a dirty change
    #     self.mark_dirty()
    #
    #     added_set = set(added)
    #     removed_set = set(removed)
    #
    #     # connect to newly added photos
    #     for photo in (added_set - self._connected_photos):
    #         photo.on_changed.connect(self._handle_photo_changed)
    #         self._connected_photos.add(photo)
    #     # disconnect and forget removed photos
    #     for photo in (self._connected_photos & removed_set):
    #         try:
    #             photo.on_changed.disconnect(self._handle_photo_changed)
    #         except Exception:
    #             # ignore if already disconnected
    #             pass
    #         self._connected_photos.remove(photo)
    #
    # def _handle_photo_changed(self) -> None:
    #     """Called when any child PhotoModel reports a change."""
    #     self.mark_dirty()
    #     self.on_changed.emit()

    def save_to_file(self, path: Union[str, Path]) -> None:
        """
        Write the serialized project JSON to the given file path.
        Parent directories will be created if necessary.
        """
        p = Path(path)
        if p.parent:
            p.parent.mkdir(parents=True, exist_ok=True)
        data = self.serialize()
        with p.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        self.mark_clean()

    def load_from_file(self, path: Union[str, Path]) -> None:
        """
        Load project JSON from the given file path and apply via deserialize().
        Raises FileNotFoundError if the path does not exist.
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(str(p))
        with p.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        self.deserialize(data)
        self.mark_clean()
