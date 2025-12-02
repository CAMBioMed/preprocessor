import logging

import cv2
import numpy as np
from cv2.typing import MatLike, Point2f

logger = logging.getLogger(__name__)


def fix_perspective(
    img: MatLike,
    src_pts: list[Point2f],
    tgt_width: int,
    tgt_height: int,
) -> MatLike:
    """Apply a perspective transformation to the input image.

    Args:
        img: The input image to be transformed.
        src_pts: A list of four points defining the source quadrilateral in the input image
            (top-left, top-right, bottom-left, bottom-right).
        tgt_width: The width of the target image, in pixels.
        tgt_height: The height of the target image, in pixels.
    """
    # tgt_height = math.sqrt(
    #     (src_pts[2][0] - src_pts[1][0]) * (src_pts[2][0] - src_pts[1][0])
    #     + (src_pts[2][1] - src_pts[1][1]) * (src_pts[2][1] - src_pts[1][1])
    # )
    # tgt_width = ratio * tgt_height
    src_pts2 = np.float32(src_pts)
    # fmt: off
    tgt_pts = np.float32([
        [      0.0,        0.0],  # top-left
        [tgt_width,        0.0],  # top-right
        [      0.0, tgt_height],  # bottom-left
        [tgt_width, tgt_height],  # bottom-right
    ])
    # fmt: on

    M = cv2.getPerspectiveTransform(src_pts2, tgt_pts)

    dst = cv2.warpPerspective(img, M, (tgt_width, tgt_height))

    return dst
