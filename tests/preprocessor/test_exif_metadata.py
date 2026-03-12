from pathlib import Path
from datetime import datetime

from preprocessor.model.project_model import ProjectModel
from preprocessor.processing.exif import extract_exif_metadata




def test_append_photo_model_populates_photo_metadata(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    photos_dir = (repo_root / "tests" / "preprocessor" / "photos").resolve()
    img1 = (photos_dir / "IMG_1054.JPG").resolve()
    assert img1.exists(), f"Example image not found: {img1}"

    # Create a temporary project file path under the repo root to ensure relative/absolute handling.
    project_file = tmp_path / "proj.pbproj"
    project_file.parent.mkdir(parents=True, exist_ok=True)

    project = ProjectModel(file=project_file)

    photo = project.append_photo_model(img1)

    # The photo metadata should have been populated from EXIF
    assert photo.metadata.camera == "Canon Canon PowerShot G9"
    assert isinstance(photo.metadata.date, datetime)
    assert photo.metadata.date == datetime(2016, 5, 29, 16, 45, 3)
    # No GPS in these example images
    assert photo.metadata.latitude is None
    assert photo.metadata.longitude is None
