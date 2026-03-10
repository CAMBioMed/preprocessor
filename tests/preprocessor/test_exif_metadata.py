from pathlib import Path
import datetime

from preprocessor.model.project_model import _extract_exif_metadata, ProjectModel


def test_extract_exif_metadata_example_images() -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    photos_dir = (repo_root / "tests" / "preprocessor" / "photos").resolve()
    img1 = (photos_dir / "IMG_1054.JPG").resolve()
    assert img1.exists(), f"Example image not found: {img1}"

    md = _extract_exif_metadata(img1)

    # Camera is constructed from Make + Model
    assert md.get('camera') == 'Canon Canon PowerShot G9'
    # Date should be a string in YYYY-MM-DD format
    assert md.get('date') == '2016-05-29'
    # No GPS in these example images
    assert md.get('latitude') is None
    assert md.get('longitude') is None


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
    assert photo.metadata.camera == 'Canon Canon PowerShot G9'
    assert isinstance(photo.metadata.date, datetime.date)
    assert photo.metadata.date == datetime.date(2016, 5, 29)
    # No GPS in these example images
    assert photo.metadata.latitude is None
    assert photo.metadata.longitude is None

