import logging

import cv2
from cv2.typing import MatLike

from preprocessor.processing.detect_quadrat import QuadratDetectionResult

logger = logging.getLogger(__name__)

def save_image(path: str, result: QuadratDetectionResult, quality: int = 95, is_rgb: bool = False) -> bool:
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
    img : MatLike | None = result.final
    if img is None:
        logger.error("No image data to save")
        return False

    ok = _save_jpeg_image(path, img, quality=q, is_rgb=is_rgb)
    if not ok:
        return False

    # Save JSON file with parameters
    json_path = f"{path}.json"
    json_data = {
        "quality": q,
        "detection": {
            "corners": list(result.corners),
        }
    }
    ok = _write_json_file(json_path, json_data)

    return ok

def _save_jpeg_image(path: str, img: MatLike, quality: int, is_rgb: bool = False) -> bool:
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
    ok = cv2.imwrite(path, img, params)

    if not ok:
        logger.error(f"Failed to save JPEG image: {path}")
    else:
        logger.debug(f"Saved JPEG image (quality={quality}): {path}")
    return bool(ok)


def _write_json_file(path: str, data: dict) -> bool:
    import json
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        logger.debug(f"Saved JSON file: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON file: {path}, error: {e}")
        return False