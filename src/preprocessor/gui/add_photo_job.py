from pathlib import Path
from typing import Optional, Any

from preprocessor.gui.qjobs import QJob
from preprocessor.utils import update_basepath
from preprocessor.model.photo_model import PhotoData


class AddPhotoJob(QJob):
    """Background job that creates a PhotoModel from a file and extracts EXIF metadata.

    This core logic is shared by the GUI and tests to avoid duplication.
    """

    result: PhotoData | None = None
    """The result of this job."""

    def __init__(self, filepath: str | Path, project_basepath: Path, name: Optional[str] = None) -> None:
        name = name or Path(filepath).name
        super().__init__(name=name)
        self._filepath = Path(filepath)
        self._project_basepath = project_basepath
        self.result = None

    def process(self) -> None:  # type: ignore[override]
        """Create PhotoData and extract EXIF metadata."""
        self.assert_not_cancelled()

        # Import here to avoid circular imports at module import time
        # Work with pydantic data objects in the worker thread (they are not QObjects)
        from preprocessor.processing.exif import extract_exif_metadata

        # Compute relative path and image dimensions without creating any QObject
        from PIL import Image

        relative_path = update_basepath(None, self._project_basepath, self._filepath)
        with Image.open(self._filepath) as img:
            width, height = img.size

        # Create PhotoData (a pydantic BaseModel) which is safe to pass across threads
        data = PhotoData(original_filename=relative_path, width=width, height=height)

        self.assert_not_cancelled()

        abs_path = (self._project_basepath / data.original_filename).resolve()
        exif_data = extract_exif_metadata(abs_path)

        # Fill metadata fields on the PhotoData.model (MetadataData)
        md = data.metadata
        md.date = exif_data.get("DateTime")
        md.photographer = exif_data.get("Photographer")
        md.camera = exif_data.get("Camera")
        md.comments = exif_data.get("Comments")
        md.latitude = exif_data.get("Latitude")
        md.longitude = exif_data.get("Longitude")

        # Return the data object; the main thread will create the PhotoModel QObject
        self.result = data
        # Report trivial progress/status
        self.update_progress(1, 1)
        self.update_status("Added")


