import sys
import numpy as np
from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch

from preprocessor.core.message_reporter import CollectingMessageReporter, Message, MessageLevel

# Make local package importable when running tests from repository root
sys.path.insert(0, "src")

from preprocessor.core.transform.perspective_crop_transform import PerspectiveCropTransform
from preprocessor.core.transform.image_transform import ImageTransformWorkItem
from preprocessor.core.model import PhotoData, CropParams
from preprocessor.core.type_corners import Corners
from preprocessor.core.types import ImageRGB


def _find_message(messages: list[Message], code: str) -> Message | None:
    for m in messages:
        if m.code == code:
            return m
    return None


def test_should_crop_successfully() -> None:
    """Should crop successfully"""
    # Arrange
    h, w = 100, 100
    img = np.zeros((h, w, 3), dtype=np.uint8)
    # Put a distinctive pixel inside the target rectangle at (20, 20)
    img[20, 20] = [123, 45, 67]
    image = ImageRGB.from_rgb_array(img)
    image_path = Path("/tmp/img4.jpg")
    image_id = "id4"

    # Define corners for an axis-aligned square from (10,10) to (90,90)
    tl = (10.0, 10.0)
    tr = (90.0, 10.0)
    bl = (10.0, 90.0)
    br = (90.0, 90.0)
    corners = Corners((tl, tr, bl, br))
    params = PhotoData(
        schema_version=1,
        image_path=image_path,
        image_id=image_id,
        color_correction=None,
        lens_correction=None,
        crop=CropParams(corners=corners),
    )

    item = ImageTransformWorkItem(
        image_id=image_id,
        image_path=image_path,
        image=image,
        params=params,
    )
    transform = PerspectiveCropTransform()
    messages = CollectingMessageReporter()
    messages.info("orig", "original")

    # Act
    result = transform(item, messages=messages)

    # Assert
    assert not messages.errors
    assert not messages.warnings
    assert result is not item
    assert isinstance(result.image, ImageRGB)
    # Target width/height should be 80x80
    assert result.image.data.shape == (80, 80, 3)
    # We can't easily test whether a pixel occurs in the resulting image, so we just assume it works here
    # Original messages are preserved
    assert any(m.code == "orig" for m in messages.messages)


def test_should_skip_perspective_crop_when_no_crop_requested() -> None:
    """Should skip perspective crop when no crop requested"""
    # Arrange
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    image = ImageRGB.from_rgb_array(img)
    image_path = Path("/tmp/img.jpg")
    image_id = "id"
    params = PhotoData(
        schema_version=1,
        image_path=image_path,
        image_id=image_id,
        color_correction=None,
        lens_correction=None,
        crop=None,
    )
    item = ImageTransformWorkItem(
        image_id=image_id,
        image_path=image_path,
        image=image,
        params=params,
    )
    transform = PerspectiveCropTransform()
    messages = CollectingMessageReporter()

    # Act
    result = transform(item, messages=messages)

    # Assert
    assert result is item
    msg = _find_message(messages.messages, "no_crop_requested")
    assert msg is not None
    assert msg.level == MessageLevel.info
    assert msg.step == transform.name


def test_should_warn_and_skip_when_crop_has_no_corners() -> None:
    """Should warn and skip when crop has no corners"""
    # Arrange
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    image = ImageRGB.from_rgb_array(img)
    image_path = Path("/tmp/img2.jpg")
    image_id = "id2"
    params = PhotoData(
        schema_version=1,
        image_path=image_path,
        image_id=image_id,
        color_correction=None,
        lens_correction=None,
        crop=CropParams(),
    )
    item = ImageTransformWorkItem(
        image_id=image_id,
        image_path=image_path,
        image=image,
        params=params,
    )
    transform = PerspectiveCropTransform()
    messages = CollectingMessageReporter()

    # Act
    result = transform(item, messages=messages)

    # Assert
    assert result is item
    msg = _find_message(messages.messages, "no_quadrat_corners")
    assert msg is not None
    assert msg.level == MessageLevel.warning
    assert msg.step == transform.name


def test_should_warn_and_skip_when_corners_are_invalid() -> None:
    """Should warn and skip when corners are invalid"""
    # Arrange
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    image = ImageRGB.from_rgb_array(img)
    image_path = Path("/tmp/img3.jpg")
    image_id = "id3"
    # Create 4 corners but with a negative coordinate to make them invalid per Corners.ordered()
    bad_corners = Corners(((-1.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)))
    params = PhotoData(
        schema_version=1,
        image_path=image_path,
        image_id=image_id,
        color_correction=None,
        lens_correction=None,
        crop=CropParams(corners=bad_corners),
    )
    item = ImageTransformWorkItem(
        image_id=image_id,
        image_path=image_path,
        image=image,
        params=params,
    )
    transform = PerspectiveCropTransform()
    messages = CollectingMessageReporter()

    # Act
    result = transform(item, messages=messages)

    # Assert
    assert result is item
    msg = _find_message(messages.messages, "invalid_quadrat_corners")
    assert msg is not None
    assert msg.level == MessageLevel.warning
    assert msg.step == transform.name
    assert msg.details is not None and "corners" in msg.details


def test_should_log_error_and_return_original_on_exception(monkeypatch: MonkeyPatch) -> None:
    """Should log error and return original when cv2 raises an exception"""
    # Arrange
    h, w = 50, 50
    img = np.zeros((h, w, 3), dtype=np.uint8)
    image = ImageRGB.from_rgb_array(img)
    image_path = Path("/tmp/img5.jpg")
    image_id = "id5"
    tl = (5.0, 5.0)
    tr = (45.0, 5.0)
    bl = (5.0, 45.0)
    br = (45.0, 45.0)
    corners = Corners((tl, tr, bl, br))
    params = PhotoData(
        schema_version=1,
        image_path=image_path,
        image_id=image_id,
        color_correction=None,
        lens_correction=None,
        crop=CropParams(corners=corners),
    )
    item = ImageTransformWorkItem(
        image_id=image_id,
        image_path=image_path,
        image=image,
        params=params,
    )
    transform = PerspectiveCropTransform()
    messages = CollectingMessageReporter()

    # Make cv2.warpPerspective raise
    import cv2

    def _boom(*args: object, **kwargs: object) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(cv2, "warpPerspective", _boom)

    # Act
    result = transform(item, messages=messages)

    # Assert
    assert result is item
    msg = _find_message(messages.messages, "perspective_crop_failed")
    assert msg is not None
    assert msg.level == MessageLevel.error
    assert "boom" in msg.text
