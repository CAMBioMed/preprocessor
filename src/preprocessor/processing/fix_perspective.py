import logging
from collections.abc import Sequence

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def fix_perspective(
    img: np.ndarray,
    src_pts: Sequence[tuple[float, float]],
) -> np.ndarray:
    """Apply a perspective transformation to the input image.

    :param img: The input image to be transformed (as a NumPy array).
    :param src_pts: A sequence of four (x, y) points defining the source quadrilateral in the
        input image. Points should be in the order: top-left, top-right, bottom-right, bottom-left
        (clockwise from the top-left).
    :return: The perspective-corrected image as a NumPy array.
    """

    # Validate input
    if src_pts is None:
        logger.error("src_pts is None")
        msg = "src_pts must be a sequence of four points"
        raise ValueError(msg)

    pts = np.asarray(src_pts, dtype=np.float32)
    if pts.shape != (4, 2):
        logger.error("src_pts must be convertible to shape (4, 2); got shape %s", pts.shape)
        msg = "src_pts must be a sequence of four (x, y) pairs"
        raise ValueError(msg)

    # Rearrange to tl, tr, bl, br
    src_pts_reordered = np.ascontiguousarray(pts[[0, 1, 3, 2], :], dtype=np.float32)
    tl, tr, bl, br = src_pts_reordered

    # Compute widths (distance between left and right points) and heights (distance between top and bottom)
    w_bottom = float(np.linalg.norm(br - bl))
    w_top = float(np.linalg.norm(tr - tl))
    h_right = float(np.linalg.norm(tr - br))
    h_left = float(np.linalg.norm(tl - bl))

    # Compute integer target dimensions; ensure at least 1 pixel in each dim.
    tgt_width = max(round(w_bottom), round(w_top), 1)
    tgt_height = max(round(h_right), round(h_left), 1)

    # Destination points: top-left, top-right, bottom-left, bottom-right
    tgt_pts = np.array(
        [
            [0.0, 0.0],
            [float(tgt_width), 0.0],
            [0.0, float(tgt_height)],
            [float(tgt_width), float(tgt_height)],
        ],
        dtype=np.float32,
    )

    try:
        M = cv2.getPerspectiveTransform(src_pts_reordered, tgt_pts)
        dst = cv2.warpPerspective(img, M, (tgt_width, tgt_height))
    except cv2.error as exc:  # pragma: no cover - backend error path
        logger.exception("OpenCV error while computing/wrapping perspective transform: %s", exc)
        raise

    return dst
