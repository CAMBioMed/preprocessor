import logging

import cv2
from cv2.typing import MatLike

logger = logging.getLogger(__name__)


def load_image(image_path: str) -> MatLike | None:
    """Load an image from the given path."""
    img = cv2.imread(image_path, cv2.IMREAD_COLOR_RGB)
    logger.debug(f"Loaded image {image_path}")
    return img  # can be None
