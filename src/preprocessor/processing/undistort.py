import contextlib
import logging
from collections.abc import Callable

from cv2.typing import MatLike

from preprocessor.model.photo_model import PhotoModel
from preprocessor.model.project_model import ProjectModel
from preprocessor.processing.load_image import load_image

logger = logging.getLogger(__name__)


def undistort_photo(
    photo: PhotoModel,
    project: ProjectModel,
    progress_callback: Callable[[float], None] | None = None,
    stop_checker: Callable[[], bool] | None = None,
) -> MatLike | None:
    """Load the photo (from project paths) and apply undistortion using the model's params.

    This function is safe to call from a worker thread. It returns the undistorted image
    (as a cv-compatible numpy array) or None on failure.

    If ``stop_checker`` is provided it will be called periodically; if it returns True
    the operation will be aborted and None returned.
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

    # Quick progress kick-off
    if progress_callback is not None:
        with contextlib.suppress(Exception):
            progress_callback(0.02)

    try:
        # We'll compute mapping and remap in chunks so we can be responsive to cancellation.
        import cv2
        import numpy as np

        h, w = img.shape[:2]
        np_camera_matrix = np.array(cam, dtype=np.float32)
        np_dist_coeffs = np.array(list(dist), dtype=np.float32)

        # Compute optimal new camera matrix (same as fix_lens_distortion.undistort)
        new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(
            np_camera_matrix,
            np_dist_coeffs,
            (w, h),
            1,
        )

        # Build remap matrices
        map1, map2 = cv2.initUndistortRectifyMap(
            np_camera_matrix,
            np_dist_coeffs,
            None,
            new_camera_matrix,
            (w, h),
            cv2.CV_32FC1,
        )

        # Prepare destination image
        dst = np.empty_like(img)

        # Chunked remap to allow cancellation and progress updates
        chunk_h = max(32, min(256, h // 8 if h >= 8 else 1))
        rows_done = 0
        y = 0
        while y < h:
            y1 = min(h, y + chunk_h)
            sub_map1 = map1[y:y1, :]
            sub_map2 = map2[y:y1, :]

            remapped = cv2.remap(img, sub_map1, sub_map2, interpolation=cv2.INTER_LINEAR)
            dst[y:y1, ...] = remapped

            rows_done = y1
            y = y1

            # progress: scale between 0.02 and 0.98 during remap
            if progress_callback is not None:
                with contextlib.suppress(Exception):
                    progress_callback(0.02 + 0.96 * (rows_done / float(h)))

            # cancellation check
            if stop_checker is not None:
                try:
                    if stop_checker():
                        logger.info("undistort_photo: stop requested for %s", original_path)
                        return None
                except Exception:
                    # swallow errors from stop_checker
                    pass

        # final undistorted image in dst
        if progress_callback is not None:
            with contextlib.suppress(Exception):
                progress_callback(1.0)

        return dst

    except Exception as exc:
        logger.exception("Failed to undistort image %s: %s", original_path, exc)
        return None
