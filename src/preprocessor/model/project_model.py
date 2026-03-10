from PySide6.QtCore import Signal
from pydantic import BaseModel, field_validator, ValidationError

from preprocessor.model.camera_model import CameraModel, CameraData
from preprocessor.model.metadata_model import MetadataModel, MetadataData
from preprocessor.model.qlistmodel import QListModel
from preprocessor.model.photo_model import PhotoModel, PhotoData

from pathlib import Path
from typing import ClassVar, Any

from preprocessor.model.qmodel import QModel
import contextlib
from PIL import Image, ExifTags
import datetime


# Helper: parse GPS coordinates from EXIF GPSInfo dict
def _parse_gps_info(gps_info: dict | None) -> tuple[str | None, str | None]:
    """Return (lat_str, lon_str) if available, else (None, None)."""
    if not gps_info:
        return None, None

    from typing import Sequence

    def _convert_to_degrees(value: Sequence[Sequence[float | int]]) -> float | None:
        # value is expected to be an iterable of 3 rational tuples like ((num, den), ...)
        try:
            # support both list/tuple containers with rationals
            d = float(value[0][0]) / float(value[0][1])
            m = float(value[1][0]) / float(value[1][1])
            s = float(value[2][0]) / float(value[2][1])
            return d + (m / 60.0) + (s / 3600.0)
        except Exception:
            return None

    # GPS tags use keys like 1=NS, 2=lat, 3=EW, 4=lon
    lat: str | None = None
    lon: str | None = None
    try:
        lat_ref: Any = gps_info.get(1) or gps_info.get('GPSLatitudeRef')
        lat_val: Any = gps_info.get(2) or gps_info.get('GPSLatitude')
        lon_ref: Any = gps_info.get(3) or gps_info.get('GPSLongitudeRef')
        lon_val: Any = gps_info.get(4) or gps_info.get('GPSLongitude')

        lat_deg: float | None = _convert_to_degrees(lat_val) if lat_val else None
        lon_deg: float | None = _convert_to_degrees(lon_val) if lon_val else None
        if lat_deg is not None and (isinstance(lat_ref, str) and lat_ref in ('S', 's')):
            lat_deg = -lat_deg
        if lon_deg is not None and (isinstance(lon_ref, str) and lon_ref in ('W', 'w')):
            lon_deg = -lon_deg
        if lat_deg is not None:
            lat = f"{lat_deg:.6f}"
        if lon_deg is not None:
            lon = f"{lon_deg:.6f}"
    except Exception:
        return None, None

    return lat, lon


def _extract_exif_metadata(path: Path) -> dict:
    """Extract common metadata from the image file using Pillow's EXIF support.

    Returns a dict with keys matching MetadataModel fields (date, photographer, camera, comments, latitude, longitude).
    """
    result: dict[str, Any] = {}
    try:
        with Image.open(path) as img:
            exif = img.getexif()
            if not exif:
                return result

            # Build a mapping from human-readable tag name to value
            tags: dict[str, Any] = {}
            for tag_id, value in exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                tags[tag] = value

            # Date
            # Common tags: DateTimeOriginal, DateTime
            date_str: Any = tags.get('DateTimeOriginal') or tags.get('DateTime')
            if date_str:
                # Date string format typically 'YYYY:MM:DD HH:MM:SS'
                try:
                    date_part: str = str(date_str).split(' ')[0]
                    date_part = date_part.replace(':', '-')
                    result['date'] = date_part  # keep as string for now; MetadataModel will accept or clean
                except Exception:
                    pass

            # Photographer/Artist
            photographer: Any = tags.get('Artist') or tags.get('Copyright')
            if photographer:
                result['photographer'] = str(photographer)

            # Camera model or make
            model: Any = tags.get('Model')
            make: Any = tags.get('Make')
            camera = None
            if make and model:
                camera = f"{make} {model}"
            elif model:
                camera = str(model)
            elif make:
                camera = str(make)
            if camera:
                result['camera'] = camera

            # Comments: ImageDescription or UserComment
            comments: Any = tags.get('ImageDescription') or tags.get('UserComment')
            if comments:
                # UserComment may be bytes
                if isinstance(comments, (bytes, bytearray)):
                    try:
                        comments = comments.decode('utf-8', errors='ignore')
                    except Exception:
                        comments = str(comments)
                result['comments'] = str(comments)

            # GPS: tags under 'GPSInfo' (numeric keys referencing GPSTAGS)
            gps_info: dict[str, Any] | None = None
            raw_gps: Any = tags.get('GPSInfo')
            if raw_gps:
                # remap numeric GPSTAGS to names for easier access
                gps_info = {}
                for k, v in raw_gps.items():
                    name = ExifTags.GPSTAGS.get(k, k)
                    gps_info[name] = v
            lat, lon = _parse_gps_info(gps_info) if gps_info else (None, None)
            if lat:
                result['latitude'] = lat
            if lon:
                result['longitude'] = lon
    except Exception:
        # Don't let EXIF extraction break the caller
        return result

    return result


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
    default_metadata: MetadataData = MetadataData()

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
    on_file_changed: Signal = Signal(Path)
    on_export_path_changed: Signal = Signal(object)
    on_target_width_changed: Signal = Signal(object)
    on_target_height_changed: Signal = Signal(object)
    on_photos_changed: Signal = Signal()
    on_cameras_changed: Signal = Signal()
    on_default_metadata_changed: Signal = Signal()

    _file: Path
    _photos: QListModel[PhotoModel]
    _cameras: QListModel[CameraModel]
    _default_metadata: MetadataModel

    def __init__(self, file: Path, data: ProjectData | dict[str, Any] | None = None) -> None:
        super().__init__(model_cls=ProjectData, data=data)

        self._file = file

        # Create QListModel containers for interactive use
        self._photos = QListModel[PhotoModel](parent=self)
        self._cameras = QListModel[CameraModel](parent=self)
        self._default_metadata = MetadataModel(data=self._data.default_metadata)

        # Track which model instances we've connected to
        self._connected_photos: set[PhotoModel] = set()
        self._connected_cameras: set[CameraModel] = set()

        # wire photos list changes to mark dirty and (re)wire photo handlers
        self._photos.bind_to_model(self, "photos", self._handle_photos_changed)
        self._cameras.bind_to_model(self, "cameras", self._handle_cameras_changed)
        self._default_metadata.on_changed.connect(self._handle_default_metadata_changed)

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
            self.on_changed.emit()

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

    @property
    def default_metadata(self) -> MetadataModel:
        """The default metadata for the project."""
        return self._default_metadata

    def _populate_lists_from_data(self) -> None:
        """
        Populate the QListModels from the current self._data (ProjectData).
        Uses the QListModel helper to reduce boilerplate.
        """
        self._photos.populate_from_data(self._data.photos, PhotoModel)
        self._cameras.populate_from_data(self._data.cameras, CameraModel)

    def _handle_photos_changed(self) -> None:
        """Handle a change in the photo models."""
        self.mark_dirty()
        with contextlib.suppress(Exception):
            self.on_photos_changed.emit()
        with contextlib.suppress(Exception):
            self.on_changed.emit()

    def _handle_cameras_changed(self) -> None:
        """Handle a change in the camera models."""
        self.mark_dirty()
        with contextlib.suppress(Exception):
            self.on_cameras_changed.emit()
        with contextlib.suppress(Exception):
            self.on_changed.emit()

    def _handle_default_metadata_changed(self) -> None:
        """Handle a change in the default metadata."""
        self.mark_dirty()
        with contextlib.suppress(Exception):
            self.on_default_metadata_changed.emit()
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
        # Ensure metadata.date fields are datetime.datetime for consistent serialization.
        try:
            for photo in self._data.photos:
                md = getattr(photo, "metadata", None)
                if md is None:
                    continue
                d = getattr(md, "date", None)
                if d is None:
                    continue
                # If it's a date (not datetime), convert to datetime at midnight
                if isinstance(d, datetime.date) and not isinstance(d, datetime.datetime):
                    md.date = datetime.datetime(d.year, d.month, d.day)
                # If it's a string, try parsing ISO date/datetime
                elif isinstance(d, str):
                    try:
                        # try full ISO datetime first
                        parsed = datetime.datetime.fromisoformat(d)
                        md.date = parsed
                    except Exception:
                        try:
                            parsed_date = datetime.date.fromisoformat(d)
                            md.date = datetime.datetime(parsed_date.year, parsed_date.month, parsed_date.day)
                        except Exception:
                            # leave as-is
                            pass
            # Default metadata too
            d = getattr(self._data.default_metadata, "date", None)
            if d is not None:
                if isinstance(d, datetime.date) and not isinstance(d, datetime.datetime):
                    self._data.default_metadata.date = datetime.datetime(d.year, d.month, d.day)
                elif isinstance(d, str):
                    try:
                        self._data.default_metadata.date = datetime.datetime.fromisoformat(d)
                    except Exception:
                        try:
                            parsed_date = datetime.date.fromisoformat(d)
                            self._data.default_metadata.date = datetime.datetime(parsed_date.year, parsed_date.month, parsed_date.day)
                        except Exception:
                            pass
        except Exception:
            # Be tolerant: if anything goes wrong, fall back to default serialization
            pass

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
        # Extract metadata from the image and populate the photo.metadata fields
        try:
            exif_data = _extract_exif_metadata(self.get_absolute_path(photo.original_filename))
            # Only set fields if they are not already set on the photo
            if 'date' in exif_data and photo.metadata.date is None:
                # Parse EXIF date string into a datetime.date when possible
                d = exif_data['date']
                if isinstance(d, str):
                    try:
                        dclean = d.replace('/', '-').replace(':', '-')
                        dclean = dclean.split(' ')[0]
                        # Convert to datetime.date
                        parsed_date = datetime.date.fromisoformat(dclean)
                        photo.metadata.date = parsed_date
                    except Exception:
                        # leave as-is (do not set) if parsing fails
                        pass
                else:
                    # If the EXIF provided a date-like object, try to coerce to date
                    try:
                        if isinstance(d, datetime.datetime):
                            photo.metadata.date = d.date()
                        elif isinstance(d, datetime.date):
                            photo.metadata.date = d
                    except Exception:
                        pass
            if 'photographer' in exif_data and photo.metadata.photographer is None:
                photo.metadata.photographer = exif_data['photographer']
            if 'camera' in exif_data and photo.metadata.camera is None:
                photo.metadata.camera = exif_data['camera']
            if 'comments' in exif_data and photo.metadata.comments is None:
                photo.metadata.comments = exif_data['comments']
            if 'latitude' in exif_data and photo.metadata.latitude is None:
                photo.metadata.latitude = exif_data['latitude']
            if 'longitude' in exif_data and photo.metadata.longitude is None:
                photo.metadata.longitude = exif_data['longitude']
        except Exception:
            # ignore metadata extraction errors
            pass

        self.photos.append(photo)
        return photo
