import logging
from pathlib import Path

import cv2
from cv2.typing import MatLike


logger = logging.getLogger(__name__)


def save_image(path: Path, img: MatLike | None, quality: int = 95, is_rgb: bool = False) -> bool:
    """
    Save image data to the given path as JPEG,
    and saves a JSON file alongside it with the same name
    containing the parameters.
    - `quality` : JPEG quality, 0-100 (higher = better)
    - `is_rgb` : Whether the input is RGB (instead of BGR)
    Returns True on success.
    """
    # Clamp quality
    q = max(0, min(100, int(quality)))

    # Save JPEG image
    if img is None:
        logger.error("No image data to save")
        return False

    ok = _save_jpeg_image(path, img, quality=q, is_rgb=is_rgb)
    return ok


def _save_jpeg_image(path: Path, img: MatLike, quality: int, is_rgb: bool = False) -> bool:
    """
    Save image data to the given path as JPEG,
    and saves a JSON file alongside it with the same name
    containing the parameters.
    - `quality` : JPEG quality, 0-100 (higher = better)
    - `is_rgb` : Whether the input is RGB (instead of BGR)
    Returns True on success.
    """
    # Handle common channel layouts
    if img.ndim == 3:
        ch = img.shape[2]
        if ch == 4 and not is_rgb:
            # BGRA -> BGR
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        elif ch == 4 and is_rgb:
            # RGBA -> BGR
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        elif ch == 3 and is_rgb:
            # RGB -> BGR
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Params for JPEG quality
    params = [cv2.IMWRITE_JPEG_QUALITY, quality]
    ok = cv2.imwrite(str(path), img, params)

    if not ok:
        logger.error(f"Failed to save JPEG image: {path}")
    else:
        logger.debug(f"Saved JPEG image (quality={quality}): {path}")
    return bool(ok)
