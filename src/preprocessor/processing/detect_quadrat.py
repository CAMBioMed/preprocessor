import logging

import cv2
from cv2.typing import MatLike

from preprocessor.processing.params import QuadratDetectionParams, DownscaleParams, BlurParams, CannyParams

logger = logging.getLogger(__name__)


def process_image(
    image_path: str | None,
    params: QuadratDetectionParams,
) -> MatLike | None:
    """Process the image and return it."""
    if not image_path:
        return None

    img = _read_image(image_path)
    if img is None:
        return None

    if params.downscale.enabled:
        img = _downscale_image(img, params.downscale)

    img = _grayscale_image(img)

    if params.blur.enabled:
        img = _blur_image(img, params.blur)

    if params.canny.enabled:
        img = _canny_image(img, params.canny)

    return img


def _read_image(image_path: str) -> MatLike | None:
    """Read the image from the given path."""
    logger.debug(f"Reading image {image_path}...")
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    logger.debug(f"Read image {image_path}")
    return img  # can be None


def _downscale_image(img: MatLike, params: DownscaleParams) -> MatLike:
    """Downscale the image to the given maximum size, for preview processing to speed up worker."""
    try:
        h, w = img.shape[:2]
        if h > params.max_size or w > params.max_size:
            scale = float(params.max_size) / float(max(h, w))
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))
            logger.debug(f"Downscaling image to {new_w}x{new_h} pixels...")
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            logger.debug(f"Downscaled image to {new_w}x{new_h} pixels")
    except Exception:
        # if resizing fails for any reason, continue with original image
        pass
    return img


def _grayscale_image(img: MatLike) -> MatLike:
    """Convert the image to grayscale."""
    logger.debug("Graying image...")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    logger.debug("Grayed image.")
    return img


def _blur_image(img: MatLike, params: BlurParams) -> MatLike:
    """Blur the image with the given kernel size."""
    logger.debug("Blurring image...")
    img = cv2.GaussianBlur(img, (params.kernel_size, params.kernel_size), 0)
    logger.debug("Blurred image")
    return img


def _canny_image(img: MatLike, params: CannyParams) -> MatLike:
    """Apply Canny edge detection to the image."""
    threshold1 = params.threshold1
    threshold2 = params.threshold2

    # WARNING: This seems to work better on the scaled down preview
    # than on the full image. Thus, generating the final image
    # full-scale will produce different results!
    logger.debug(f"Cannying image to {threshold1}, {threshold2}...")
    img = cv2.Canny(img, threshold1, threshold2, apertureSize=params.aperture_size)
    logger.debug("Cannied image.")
    return img
