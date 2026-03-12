from datetime import datetime
from pathlib import Path

from preprocessor.processing.exif import extract_exif_metadata

repo_root = Path(__file__).resolve().parent.parent.parent
photos_dir = (repo_root / "tests" / "preprocessor" / "photos").resolve()

def test_extract_exif_metadata_1() -> None:
    img1 = (photos_dir / "IMG_1054.JPG").resolve()
    assert img1.exists(), f"Example image not found: {img1}"

    md = extract_exif_metadata(img1)

    assert md.get("Camera") == "Canon Canon PowerShot G9"
    assert md.get("DateTime") == datetime(2016, 5, 29, 16, 45, 3)
    assert md.get("Latitude") is None
    assert md.get("Longitude") is None

def test_extract_exif_metadata_2() -> None:
    img1 = (photos_dir / "gpstest.JPG").resolve()
    assert img1.exists(), f"Example image not found: {img1}"

    md = extract_exif_metadata(img1)

    assert md.get("Camera") == "Google Pixel 7a"
    assert md.get("DateTime") == datetime(2025, 4, 3, 19, 38, 5)
    assert abs(md.get("Latitude") - 35.520042) < 1e-6  # type: ignore[operator]
    assert abs(md.get("Longitude") - 24.019297) < 1e-6  # type: ignore[operator]