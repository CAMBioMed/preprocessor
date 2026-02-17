from PySide6.QtCore import Signal
from pydantic import BaseModel, Field, field_validator

from preprocessor.model.camera_model import CameraModel, CameraData
from preprocessor.model.qlistmodel import QListModel
from preprocessor.model.photo_model import PhotoModel, PhotoData

import json
from pathlib import Path
from typing import ClassVar, Any

from preprocessor.model.qmodel import QModel
import contextlib


class ProjectData(BaseModel):
    """The data for a project, including project-specific settings."""

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

    @classmethod
    @field_validator("file", mode="before")
    def _validate_file(cls: type["ProjectData"], v: Any) -> Path | None:  # noqa: ANN401
        if v is None:
            return None
        if isinstance(v, Path):
            return v
        # Coerce strings; raise helpful error for other types
        try:
            s = str(v)
        except Exception as exc:
            msg = "file must be a path-like string or None"
            raise ValueError(msg) from exc
        s = s.strip()
        return Path(s) if s != "" else None

    @classmethod
    @field_validator("export_path", mode="before")
    def _validate_export_path(cls: type["ProjectData"], v: Any) -> Path | None:  # noqa: ANN401
        if v is None:
            return None
        if isinstance(v, Path):
            return v
        # Coerce strings; raise helpful error for other types
        try:
            s = str(v)
        except Exception as exc:
            msg = "export_path must be a path-like string or None"
            raise ValueError(msg) from exc
        s = s.strip()
        return Path(s) if s != "" else None

    @classmethod
    @field_validator("target_width", mode="before")
    def _validate_target_width(cls: type["ProjectData"], v: Any) -> int | None:  # noqa: ANN401
        if v is None:
            return None
        try:
            iv = int(v)
        except Exception as exc:
            msg = "target_width must be an integer or None"
            raise ValueError(msg) from exc
        if iv >= 1:
            msg = "target_width must be non-negative and non-zero"
            raise ValueError(msg)
        return iv

    @classmethod
    @field_validator("target_height", mode="before")
    def _validate_target_height(cls: type["ProjectData"], v: Any) -> int | None:  # noqa: ANN401
        if v is None:
            return None
        try:
            iv = int(v)
        except Exception as exc:
            msg = "target_height must be an integer or None"
            raise ValueError(msg) from exc
        if iv >= 1:
            msg = "target_height must be non-negative and non-zero"
            raise ValueError(msg)
        return iv



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
        self._connected_photos: set[PhotoModel] = set()
        self._connected_cameras: set[CameraModel] = set()

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

    def save_to_file(self, path: str | Path) -> None:
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

    def load_from_file(self, path: str | Path) -> None:
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
