import contextlib
import logging
from typing import Optional, Callable

from cv2.typing import MatLike

from preprocessor.model.photo_model import PhotoModel
from preprocessor.model.project_model import ProjectModel
from preprocessor.processing.fix_lens_distortion import undistort
from preprocessor.processing.load_image import load_image

logger = logging.getLogger(__name__)

def undistort_photo(
    photo: PhotoModel,
    project: ProjectModel,
    progress_callback: Optional[Callable[[float], None]] = None,
) -> MatLike | None:
    """Load the photo (from project paths) and apply undistortion using the model's params.

    This function is safe to call from a worker thread. It returns the undistorted image
    (as a cv-compatible numpy array) or None on failure.
    """
    # Try to obtain camera/distortion parameters
    cam = getattr(photo, "camera_matrix", None)
    dist = getattr(photo, "distortion_coefficients", None)
    if cam is None or dist is None:
        return None

    # Load the image from disk
    original_path = project.get_absolute_path(photo.original_filename)
    img = load_image(str(original_path))
    if img is None:
        logger.error("Failed to load image %s", original_path)
        return None

    # Optionally report progress (simple two-step progress)
    if progress_callback is not None:
        with contextlib.suppress(Exception):
            progress_callback(0.2)

    try:
        und = undistort(img, cam, list(dist))
    except Exception as exc:
        logger.exception("Failed to undistort image %s: %s", original_path, exc)
        return None

    if progress_callback is not None:
        with contextlib.suppress(Exception):
            progress_callback(1.0)

    return und

