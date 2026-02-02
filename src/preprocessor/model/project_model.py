from PySide6.QtCore import QObject, Signal

from preprocessor.model.list_model import QListModel
from preprocessor.model.photo_model import PhotoModel

# Add imports for file IO
import json
from pathlib import Path
from typing import Union, Set, Iterable


class ProjectModel(QObject):
    """
    The model for the entire current project.

    This includes the project-specific settings.
    """

    # serialization version for the project JSON format
    SERIAL_VERSION: int = 1

    on_changed: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()
        # store the photos list on the instance
        self._photos = QListModel[PhotoModel](parent = self)

        # track which PhotoModel instances we've connected to
        self._connected_photos: Set[PhotoModel] = set()

        # wire photos list changes to mark dirty and (re)wire photo handlers
        self.photos.on_changed.connect(self._on_photos_changed)
        # wire any existing photos without generating a photos-changed event / dirty mark
        for photo in list(self.photos):
            photo.on_changed.connect(self._on_photo_changed)
            self._connected_photos.add(photo)

    _file_path: Path | None = None
    on_file_path_changed: Signal = Signal(object)

    @property
    def file_path(self) -> Path | None:
        """
        The file path where the project is saved, or None if not saved yet.

        This property is not serialized/deserialized.
        """
        return self._file_path

    @file_path.setter
    def file_path(self, path: Path | None) -> None:
        old_path = self._file_path
        if old_path != path:
            self._file_path = path
            self.on_file_path_changed.emit(path)

    _photos: QListModel[PhotoModel]

    @property
    def photos(self) -> QListModel[PhotoModel]:
        """The list of photos in the project."""
        return self._photos

    _dirty: bool = False
    on_dirty_changed: Signal = Signal(bool)

    @property
    def dirty(self) -> bool:
        """Whether the project has unsaved changes."""
        return self._dirty

    def _set_dirty(self, value: bool) -> None:
        if self._dirty != value:
            self._dirty = value
            self.on_dirty_changed.emit(value)
            self.on_changed.emit()

    def mark_clean(self) -> None:
        """Mark the project as clean (no unsaved changes)."""
        self._set_dirty(False)

    def mark_dirty(self) -> None:
        """Mark the project as dirty (has unsaved changes)."""
        self._set_dirty(True)

    # internal handlers for wiring child signals
    def _on_photos_changed(self, added: Iterable[PhotoModel], removed: Iterable[PhotoModel]) -> None:
        """
        Called when the photos QListModel changes.
        Marks project dirty and (re)wires per-photo on_changed handlers.
        """
        # any modification to the list counts as a dirty change
        self.mark_dirty()

        added_set = set(added)
        removed_set = set(removed)

        # connect to newly added photos
        for photo in (added_set - self._connected_photos):
            photo.on_changed.connect(self._on_photo_changed)
            self._connected_photos.add(photo)
        # disconnect and forget removed photos
        for photo in (self._connected_photos & removed_set):
            try:
                photo.on_changed.disconnect(self._on_photo_changed)
            except Exception:
                # ignore if already disconnected
                pass
            self._connected_photos.remove(photo)

    def _on_photo_changed(self) -> None:
        """Called when any child PhotoModel reports a change."""
        self.mark_dirty()
        self.on_changed.emit()

    def serialize(self) -> dict:
        """
        Serialize this model into basic Python types suitable for JSON.
        """
        # Serialize each PhotoModel using its serialize() method
        return {
            "version": self.SERIAL_VERSION,
            "photos": [p.serialize() for p in self.photos],
        }

    def deserialize(self, data: dict) -> None:
        """
        Deserialize state from a dict produced by serialize.
        Uses the setters so signals are emitted only on change.
        If a key doesn't occur in the data, it is not set.
        """
        # Validate serialization version
        ver = data.get("version", None)
        if ver != self.SERIAL_VERSION:
            raise ValueError(f"Unsupported project version: {ver!r}, expected {self.SERIAL_VERSION}")

        if "photos" in data:
            photos_raw = data.get("photos", None)
            # If explicit None -> clear list
            if photos_raw is None:
                # remove existing photos
                # clear the QListModel by removing items
                # iterate copy to avoid modification during iteration
                for item in list(self.photos):
                    self.photos.remove(item)
                # Signal that project changed
                self.on_changed.emit()
            else:
                # Expecting iterable of dicts
                # Clear existing photos first
                for item in list(self.photos):
                    self.photos.remove(item)
                # Recreate PhotoModel instances from serialized data
                for pic_data in photos_raw:
                    photo = PhotoModel()
                    # Let the photo deserialize itself (will emit its own signals)
                    photo.deserialize(pic_data)
                    self.photos.append(photo)
                # Signal that project changed
                self.on_changed.emit()

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
