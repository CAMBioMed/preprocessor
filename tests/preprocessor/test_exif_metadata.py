from pathlib import Path
from datetime import datetime

from preprocessor.gui.jobs.add_photo_job import AddPhotoJob


def test_append_photo_model_populates_photo_metadata(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    photos_dir = (repo_root / "tests" / "preprocessor" / "photos").resolve()
    img1 = (photos_dir / "IMG_1054.JPG").resolve()
    assert img1.exists(), f"Example image not found: {img1}"

    # Create a temporary project file path under the repo root to ensure relative/absolute handling.
    project_file = tmp_path / "proj.pbproj"
    project_file.parent.mkdir(parents=True, exist_ok=True)

    # Use the shared AddPhotoJob implementation
    job = AddPhotoJob(img1)
    job.process()
    photo = job.result

    # The photo metadata should have been populated from EXIF
    assert photo is not None
    assert photo.metadata.camera == "Canon Canon PowerShot G9"
    assert isinstance(photo.metadata.date, datetime)
    assert photo.metadata.date == datetime(2016, 5, 29, 16, 45, 3)
    # No GPS in these example images
    assert photo.metadata.latitude is None
    assert photo.metadata.longitude is None
