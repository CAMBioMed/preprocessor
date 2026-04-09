import sys
from pathlib import Path
from typing import override

import numpy as np

from _pytest.monkeypatch import MonkeyPatch

from preprocessor.core.progress_reporter import ProgressReporter, NOOP_PROGRESS_REPORTER

# Make local package importable when running tests from repository root
sys.path.insert(0, "src")

from preprocessor.core.transform.transform_image import transform_image
from preprocessor.core.message_reporter import CollectingMessageReporter, MessageReporter, NOOP_MESSAGE_REPORTER
from preprocessor.core.types import ImageRGB
from preprocessor.core.transform.image_transform import ImageTransformWorkItem, ImageTransform
from preprocessor.core.model import PhotoData


class _IdentityTransform(ImageTransform):
    name = "identity"

    @override
    def __call__(
        self,
        item: ImageTransformWorkItem,
        /,
        *,
        messages: MessageReporter = NOOP_MESSAGE_REPORTER,
        progress: ProgressReporter = NOOP_PROGRESS_REPORTER,
    ) -> ImageTransformWorkItem:
        # Return a new work item (copy-like) to simulate a real transform that may
        # produce a new ImageTransformWorkItem instance.
        return ImageTransformWorkItem(
            image_id=item.image_id,
            image_path=item.image_path,
            image=item.image,
            params=item.params,
        )


class _BadTransform(ImageTransform):
    name = "bad"

    @override
    def __call__(
        self,
        item: ImageTransformWorkItem,
        /,
        *,
        messages: MessageReporter = NOOP_MESSAGE_REPORTER,
        progress: ProgressReporter = NOOP_PROGRESS_REPORTER,
    ) -> ImageTransformWorkItem:
        raise RuntimeError("boom")


def test_should_return_none_and_report_error_when_image_load_fails(monkeypatch: MonkeyPatch) -> None:
    """should return None and report error when image load fails"""
    # Arrange
    image_path = Path("/nonexistent/path.jpg")
    image_id = "path"
    params = PhotoData(
        schema_version=1,
        image_path=image_path,
        image_id=image_id,
        color_correction=None,
        lens_correction=None,
        crop=None,
    )
    messages = CollectingMessageReporter()

    # Make ImageRGB.from_file raise
    def _boom(path: Path) -> None:
        raise RuntimeError("load failed")

    monkeypatch.setattr(ImageRGB, "from_file", staticmethod(_boom))

    # Act
    result = transform_image(image_path, params, output_path=None, transforms=[], messages=messages)

    # Assert
    assert result is None
    # There should be exactly one error message with code image_load_failed
    errors = [m for m in messages.messages if m.code == "image_load_failed"]
    assert errors, "expected an image_load_failed error message"


def test_should_apply_transforms_and_save_output(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    """should apply transforms and save output when transforms succeed and output path given"""
    # Arrange
    h, w = 10, 10
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    # set a pixel to make the image non-empty
    arr[1, 1] = [1, 2, 3]
    image = ImageRGB.from_rgb_array(arr)
    image_path = Path("/tmp/img.jpg")
    image_id = "img"
    params = PhotoData(
        schema_version=1,
        image_path=image_path,
        image_id=image_id,
        color_correction=None,
        lens_correction=None,
        crop=None,
    )
    messages = CollectingMessageReporter()

    # Monkeypatch loading to return our in-memory image
    monkeypatch.setattr(ImageRGB, "from_file", staticmethod(lambda p: image))

    # Monkeypatch ImageRGB.to_file to write a small placeholder so filesystem check passes
    def _to_file(self: ImageRGB, path: Path) -> None:
        path.write_bytes(b"ok")

    monkeypatch.setattr(ImageRGB, "to_file", _to_file, raising=False)

    output_path = tmp_path / "out.jpg"

    # Act
    result = transform_image(
        image_path,
        params,
        output_path=output_path,
        transforms=[_IdentityTransform()],
        messages=messages,
    )

    # Assert
    assert result is not None
    assert isinstance(result, ImageRGB)
    assert output_path.exists()
    assert not messages.has_errors


def test_should_report_transform_failed_and_return_none_when_transform_raises(monkeypatch: MonkeyPatch) -> None:
    """should return None and report transform_failed when a transform raises"""
    # Arrange
    h, w = 5, 5
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    image = ImageRGB.from_rgb_array(arr)
    image_path = Path("/tmp/img2.jpg")
    image_id = "img2"
    params = PhotoData(
        schema_version=1,
        image_path=image_path,
        image_id=image_id,
        color_correction=None,
        lens_correction=None,
        crop=None,
    )
    messages = CollectingMessageReporter()

    monkeypatch.setattr(ImageRGB, "from_file", staticmethod(lambda p: image))

    # Act
    result = transform_image(image_path, params, output_path=None, transforms=[_BadTransform()], messages=messages)

    # Assert
    assert result is None
    errs = [m for m in messages.messages if m.code == "transform_failed"]
    assert errs, "expected a transform_failed message"


def test_should_report_image_save_failed_and_return_none_when_save_raises(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """should return None and report image_save_failed when saving the image fails"""
    # Arrange
    h, w = 6, 6
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    image = ImageRGB.from_rgb_array(arr)
    image_path = Path("/tmp/img3.jpg")
    image_id = "img3"
    params = PhotoData(
        schema_version=1,
        image_path=image_path,
        image_id=image_id,
        color_correction=None,
        lens_correction=None,
        crop=None,
    )
    messages = CollectingMessageReporter()

    monkeypatch.setattr(ImageRGB, "from_file", staticmethod(lambda p: image))

    def _to_file_fail(self: ImageRGB, path: Path) -> None:
        raise RuntimeError("disk full")

    monkeypatch.setattr(ImageRGB, "to_file", _to_file_fail, raising=False)

    output_path = tmp_path / "out2.jpg"

    # Act
    result = transform_image(
        image_path,
        params,
        output_path=output_path,
        transforms=[_IdentityTransform()],
        messages=messages,
    )

    # Assert
    assert result is None
    errs = [m for m in messages.messages if m.code == "image_save_failed"]
    assert errs, "expected an image_save_failed message"
