import logging
import math

import cv2
import numpy as np
from cv2.typing import MatLike

from preprocessor.processing.params import (
    QuadratDetectionParams,
    DownscaleParams,
    BlurParams,
    CannyParams,
    ThresholdingParams,
    ThresholdingMethod,
    FindContourParams,
    ContourApproximationMethod,
    HoughParams,
)

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

    # Create transparent empty image
    debug_img = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)

    if params.blur.enabled:
        img = _blur_image(img, params.blur)

    if params.thresholding.method != ThresholdingMethod.NONE:
        img = _threshold_image(img, params.thresholding)

    if params.canny.enabled:
        img = _canny_image(img, params.canny)

    if params.hough.enabled:
        debug_img = _hough(img, debug_img, params.hough)

    if params.findContour.enabled:
        debug_img = _find_contours(img, debug_img, params.findContour)

    # Draw debug image on top of original
    bgr_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    bgr_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2BGRA)
    img = cv2.addWeighted(bgr_img, 0.7, debug_img, 0.3, 0)  # semi-transparent
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


def _threshold_image(img: MatLike, params: ThresholdingParams) -> MatLike:
    """Apply thresholding to the image."""
    method = params.method
    threshold = params.threshold
    maximum = params.maximum
    block_size = params.block_size
    C = params.C

    logger.debug(f"Thresholding image with method {method}...")
    if method == ThresholdingMethod.NONE:
        return img
    if method == ThresholdingMethod.BINARY:
        if params.inverse:
            _, img = cv2.threshold(img, threshold, maximum, cv2.THRESH_BINARY_INV)
        else:
            _, img = cv2.threshold(img, threshold, maximum, cv2.THRESH_BINARY)
    elif method == ThresholdingMethod.TRUNC:
        _, img = cv2.threshold(img, threshold, 0, cv2.THRESH_TRUNC)
    elif method == ThresholdingMethod.TO_ZERO:
        if params.inverse:
            _, img = cv2.threshold(img, threshold, 0, cv2.THRESH_TOZERO_INV)
        else:
            _, img = cv2.threshold(img, threshold, 0, cv2.THRESH_TOZERO)
    elif method == ThresholdingMethod.MEAN:
        if params.inverse:
            img = cv2.adaptiveThreshold(img, maximum, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, block_size, C)
        else:
            img = cv2.adaptiveThreshold(img, maximum, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)
    elif method == ThresholdingMethod.GAUSSIAN:
        if params.inverse:
            img = cv2.adaptiveThreshold(
                img, maximum, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, C
            )
        else:
            img = cv2.adaptiveThreshold(img, maximum, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)
    else:
        msg = f"Unknown thresholding method: {method}"
        logger.error(msg)
        raise NotImplementedError(msg)

    logger.debug("Thresholded image.")
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


def _hough(img: MatLike, debug_img: MatLike, params: HoughParams) -> MatLike:
    """Apply Hough Transform to detect lines in the image."""
    logger.debug("Applying Hough Transform...")
    if params.probabilistic:
        lines = cv2.HoughLinesP(
            img,
            rho=params.rho,
            theta=math.radians(params.theta),
            threshold=params.threshold,
            minLineLength=params.min_line_length,
            maxLineGap=params.max_line_gap,
        )
        if lines is not None:
            logger.debug(f"Found {len(lines)} lines.")
            for i in range(len(lines)):
                x1, y1, x2, y2 = lines[i][0]
                pt1 = (x1, y1)
                pt2 = (x2, y2)
                cv2.line(debug_img, pt1, pt2, (0, 255, 0), 1, cv2.LINE_AA)
        else:
            logger.debug("No lines found.")
    else:
        lines = cv2.HoughLines(
            img,
            rho=params.rho,
            theta=math.radians(params.theta),
            threshold=params.threshold,
            srn=params.srn,
            stn=params.stn,
            min_theta=math.radians(params.min_theta),
            max_theta=math.radians(params.max_theta),
        )
        if lines is not None:
            logger.debug(f"Found {len(lines)} lines.")
            for i in range(len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
                pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))
                cv2.line(debug_img, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            logger.debug("No lines found.")
    return debug_img


def _find_contours(img: MatLike, debug_img: MatLike, params: FindContourParams) -> MatLike:
    """Find contours in the image."""
    logger.debug("Finding contours...")
    method: int
    if params.method == ContourApproximationMethod.NONE:
        method = cv2.CHAIN_APPROX_NONE
    elif params.method == ContourApproximationMethod.SIMPLE:
        method = cv2.CHAIN_APPROX_SIMPLE
    elif params.method == ContourApproximationMethod.TC89_L1:
        method = cv2.CHAIN_APPROX_TC89_L1
    elif params.method == ContourApproximationMethod.TC89_KCOS:
        method = cv2.CHAIN_APPROX_TC89_KCOS
    else:
        msg = f"Unknown contour approximation method: {params.method}"
        logger.error(msg)
        raise NotImplementedError(msg)

    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, method)
    logger.debug(f"Found {len(contours)} contours.")
    debug_img = cv2.drawContours(debug_img, contours, -1, (0, 255, 0), 2)
    return debug_img
