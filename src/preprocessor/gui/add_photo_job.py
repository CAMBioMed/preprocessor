from pathlib import Path
from typing import Optional, Any

from preprocessor.gui.qjobs import QJob


class AddPhotoJob(QJob):
    """Background job that creates a PhotoModel from a file and extracts EXIF metadata.

    This core logic is shared by the GUI and tests to avoid duplication.
    """

    result_photo: Any | None = None

    def __init__(self, filepath: str | Path, project_basepath: Path, name: Optional[str] = None) -> None:
        name = name or Path(filepath).name
        super().__init__(name=name)
        self._filepath = Path(filepath)
        self._project_basepath = project_basepath
        self.result_photo = None

    def process(self) -> bool:  # type: ignore[override]
        """Perform the work: create PhotoModel and extract EXIF metadata.

        Returns False on success, True if aborted/failed.
        """
        try:
            # Import here to avoid circular imports at module import time
            from preprocessor.model.photo_model import PhotoModel
            from preprocessor.processing.exif import extract_exif_metadata

            photo = PhotoModel.from_file(self._filepath, self._project_basepath)

            abs_path = (self._project_basepath / photo.original_filename).resolve()
            exif_data = extract_exif_metadata(abs_path)

            photo.metadata.date = exif_data.get("DateTime")
            photo.metadata.photographer = exif_data.get("Photographer")
            photo.metadata.camera = exif_data.get("Camera")
            photo.metadata.comments = exif_data.get("Comments")
            photo.metadata.latitude = exif_data.get("Latitude")
            photo.metadata.longitude = exif_data.get("Longitude")

            self.result_photo = photo
            # Report trivial progress/status
            self.update_progress(1, 1)
            self.update_status("Loaded")
            return False
        except Exception as exc:  # pragma: no cover - difficult to trigger in tests
            # Signal failure via status and indicate aborted
            self.update_status(f"Error: {exc!s}")
            return True


