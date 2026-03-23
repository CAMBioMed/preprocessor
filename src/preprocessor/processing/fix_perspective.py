import logging
from math import sqrt

import cv2
import numpy as np
from cv2.typing import MatLike, Point2f

logger = logging.getLogger(__name__)


def fix_perspective(
    img: MatLike,
    src_pts: list[Point2f],
) -> MatLike:
    """Apply a perspective transformation to the input image.

    :param img: The input image to be transformed.
    :param src_pts: A list of four points defining the source quadrilateral in the input image
        (top-left, top-right, bottom-right, bottom-left) (clockwise from the top-left).
    :return: The perspective-corrected image.
    """

    src_pts2 = np.float32(src_pts)
    src_pts3 = src_pts2[[0, 1, 3, 2]]  # rearrange to tl, tr, bl, br

    # Compute the maximum widths and heights of the target rectangle based on the source points
    tl, tr, bl, br = src_pts3
    w1 = sqrt((br[0] - bl[0])**2 + (br[0] - bl[0])**2)
    w2 = sqrt((tr[0] - tl[0])**2 + (tr[0] - tl[0])**2)
    h1 = sqrt((tr[1] - br[1])**2 + (tr[1] - br[1])**2)
    h2 = sqrt((tl[1] - bl[1])**2 + (tl[1] - bl[1])**2)
    tgt_width = int(max(w1, w2))
    tgt_height = int(max(h1, h2))

    # fmt: off
    tgt_pts = np.float32([
        [      0.0,        0.0],  # top-left
        [tgt_width,        0.0],  # top-right
        [      0.0, tgt_height],  # bottom-left
        [tgt_width, tgt_height],  # bottom-right
    ])
    # fmt: on

    M = cv2.getPerspectiveTransform(src_pts3, tgt_pts)

    dst = cv2.warpPerspective(img, M, (tgt_width, tgt_height))

    return dst
