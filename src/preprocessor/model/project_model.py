from PySide6.QtCore import Signal
from pydantic import BaseModel, field_validator, ValidationError

from preprocessor.model.camera_model import CameraModel, CameraData
from preprocessor.model.qlistmodel import QListModel
from preprocessor.model.photo_model import PhotoModel, PhotoData

from pathlib import Path
from typing import ClassVar, Any

from preprocessor.model.qmodel import QModel
import contextlib

from preprocessor.utils import update_basepath


class ProjectData(BaseModel):
    """The data for a project, including project-specific settings."""

    # Serialization JSON version
    SERIAL_VERSION: ClassVar[int] = 1

    model_version: int = SERIAL_VERSION
    """The version of the data model, used for compatibility checks during deserialization."""
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

    @field_validator("model_version", mode="after")
    @classmethod
    def _validate_model_version(cls: type["ProjectData"], v: int) -> int:
        if v != cls.SERIAL_VERSION:
            msg = f"Unsupported model_version {v}; expected {cls.SERIAL_VERSION}"
            raise ValueError(msg)
        return v

    @field_validator("target_width", mode="after")
    @classmethod
    def _validate_target_width(cls: type["ProjectData"], v: int | None) -> int | None:
        if v is not None and v < 1:
            msg = "target_width must be non-negative and non-zero"
            raise ValueError(msg)
        return v

    @field_validator("target_height", mode="after")
    @classmethod
    def _validate_target_height(cls: type["ProjectData"], v: int | None) -> int | None:
        if v is not None and v < 1:
            msg = "target_height must be non-negative and non-zero"
            raise ValueError(msg)
        return v


class ProjectModel(QModel[ProjectData]):
    on_file_changed: Signal = Signal(object)
    on_export_path_changed: Signal = Signal(object)
    on_target_width_changed: Signal = Signal(object)
    on_target_height_changed: Signal = Signal(object)

    _file: Path
    _photos: QListModel[PhotoModel]
    _cameras: QListModel[CameraModel]

    def __init__(self, file: Path, data: ProjectData | dict[str, Any] | None = None) -> None:
        super().__init__(model_cls=ProjectData, data=data)

        self._file = file

        # Create QListModel containers for interactive use
        self._photos = QListModel[PhotoModel](parent=self)
        self._cameras = QListModel[CameraModel](parent=self)

        # Track which model instances we've connected to
        self._connected_photos: set[PhotoModel] = set()
        self._connected_cameras: set[CameraModel] = set()

        # wire photos list changes to mark dirty and (re)wire photo handlers
        self._photos.bind_to_model(self, "photos", self._handle_child_changed)
        self._cameras.bind_to_model(self, "cameras", self._handle_child_changed)

        self._populate_lists_from_data()

    @property
    def file(self) -> Path:
        """
        The file path where the project is or will be saved.

        This property is not serialized/deserialized.
        """
        return self._file

    @file.setter
    def file(self, path: Path) -> None:
        if self._file != path:
            old_path = self._file
            self._file = path
            self.update_paths_relative_to(old_basepath=old_path.parent, new_basepath=path.parent)
            self.on_file_changed.emit(path)

    @property
    def export_path(self) -> Path | None:
        """The file path where the photos will be exported to, or None if not set."""
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

    def _populate_lists_from_data(self) -> None:
        """
        Populate the QListModels from the current self._data (ProjectData).
        Uses the QListModel helper to reduce boilerplate.
        """
        self._photos.populate_from_data(self._data.photos, PhotoModel)
        self._cameras.populate_from_data(self._data.cameras, CameraModel)

    def _handle_child_changed(self) -> None:
        """Handle a child model reporting a change."""
        self.mark_dirty()
        with contextlib.suppress(Exception):
            self.on_changed.emit()

    def update_paths_relative_to(self, old_basepath: Path, new_basepath: Path) -> None:
        for photo in self._photos:
            photo.update_paths_relative_to(old_basepath, new_basepath)
        for camera in self._cameras:
            camera.update_paths_relative_to(old_basepath, new_basepath)

    def write_to_file(self, path: str | Path) -> None:
        """
        Write the serialized project JSON to the given file path.
        Parent directories will be created if necessary.
        """
        p = Path(path)
        if p.parent:
            p.parent.mkdir(parents=True, exist_ok=True)
        # First we update the `file` attribute, so that all other paths in the project are updated accordingly
        self.file = Path(path)
        # Only then do we write out the changes
        json_str = self.write_to_json()
        with p.open("w", encoding="utf-8") as fh:
            fh.write(json_str)
        self.mark_clean()

    def write_to_json(self) -> str:
        """Return a JSON string representation of the model."""
        return self._data.model_dump_json(indent=2)

    @classmethod
    def read_from_file(cls: type["ProjectModel"], path: str | Path) -> "ProjectModel":
        """
        Load project JSON from the given file path and apply via deserialize().
        Raises FileNotFoundError if the path does not exist.
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(str(p))
        with p.open("r", encoding="utf-8") as fh:
            json_str = fh.read()
        return cls.read_from_json(path, json_str)

    @classmethod
    def read_from_json(cls: type["ProjectModel"], path: str | Path, json_str: str) -> "ProjectModel":
        """Load model data from a JSON string."""
        try:
            new_data = ProjectData.model_validate_json(json_str)  # type: ignore[arg-type]
        except ValidationError as exc:
            raise ValueError(str(exc)) from exc

        return ProjectModel(file=Path(path), data=new_data)

    def get_absolute_path(self, path: Path) -> Path:
        """Get the absolute file path of the photo, resolved from original_filename relative to the given basepath."""
        return (self.file.parent / path).resolve()

    def append_photo_model(self, path: Path) -> PhotoModel:
        """Helper function to create a new PhotoModel with the given path and add it to the project."""
        photo = PhotoModel.from_file(path, self.file.parent)
        self.photos.append(photo)
        return photo

    def _get_image_dimensions(self, path: Path) -> tuple[int, int]:
        from PIL import Image

        with Image.open(path) as img:
            return img.height, img.width
