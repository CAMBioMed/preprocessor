import numpy as np

from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch

from preprocessor.core.lens_correct_transform import LensCorrectTransform
from preprocessor.core.image_transform import ImageTransformWorkItem
from preprocessor.core.types import ImageRGB
from preprocessor.core.photo_params import PhotoParams, LensCorrectionParams


def test_should_skip_lens_correction_when_no_lens_correction_requested() -> None:
	"""Should skip lens correction when no lens correction requested"""
	# Arrange
	h, w = 32, 48
	arr = np.zeros((h, w, 3), dtype=np.uint8)
	image = ImageRGB.from_rgb_array(arr)
	params = PhotoParams(schema_version=1, color_correction=None, lens_correction=None, crop=None)
	item = ImageTransformWorkItem(
		image_id="img1",
		image_path=Path("/tmp/img1.jpg"),
		image=image,
		params=params,
	)

	# Act
	out = LensCorrectTransform()(item)

	# Assert
	# Should return the same work item and add an info message indicating skip
	assert out is item
	assert any(m.code == "no_lens_correction_requested" for m in out.messages)


def test_should_return_transformed_image_when_lens_correction_requested() -> None:
	"""Should return transformed image when lens correction requested"""
	# Arrange
	h, w = 64, 64
	# simple test image: horizontal gradient
	arr = np.tile(np.arange(w, dtype=np.uint8), (h, 1))
	rgb = np.stack([arr, arr, arr], axis=2)
	image = ImageRGB.from_rgb_array(rgb)
	lens_params = LensCorrectionParams(camera_matrix=None, coefficients=[0.0, 0.0, 0.0, 0.0])
	params = PhotoParams(schema_version=1, color_correction=None, lens_correction=lens_params, crop=None)
	item = ImageTransformWorkItem(
		image_id="img2",
		image_path=Path("/tmp/img2.jpg"),
		image=image,
		params=params,
	)

	# Act
	out = LensCorrectTransform()(item)

	# Assert
	# Should return a new work item with an ImageRGB of the same shape and no errors
	assert out is not item
	assert isinstance(out.image, ImageRGB)
	assert out.image.data.shape == image.data.shape
	assert out.get_errors() == []


def test_should_return_original_and_error_when_cv2_raises(monkeypatch: MonkeyPatch) -> None:
	"""Should return original work item and add an error when cv2 raises during transform"""
	# Arrange
	h, w = 32, 32
	arr = np.zeros((h, w, 3), dtype=np.uint8)
	image = ImageRGB.from_rgb_array(arr)
	lens_params = LensCorrectionParams(camera_matrix=None, coefficients=[0.0, 0.0, 0.0, 0.0])
	params = PhotoParams(schema_version=1, color_correction=None, lens_correction=lens_params, crop=None)
	item = ImageTransformWorkItem(
		image_id="img3",
		image_path=Path("/tmp/img3.jpg"),
		image=image,
		params=params,
	)

	# Force cv2.getOptimalNewCameraMatrix to raise
	import preprocessor.core.lens_correct_transform as lct_mod

	def _boom(*args: object, **kwargs: object) -> None:
		raise RuntimeError("boom")

	monkeypatch.setattr(lct_mod.cv2, "getOptimalNewCameraMatrix", _boom)

	# Act
	out = LensCorrectTransform()(item)

	# Assert
	# The transform should catch the exception, attach an error message and return the original item
	assert out is item
	assert any(m.code == "lens_correction_failed" for m in out.messages)



