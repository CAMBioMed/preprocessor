import logging
import math
from dataclasses import dataclass
from typing import cast

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


@dataclass
class QuadratDetectionResult:
    original: MatLike | None
    processed: MatLike | None
    debug: MatLike | None


def process_image(
    image_path: str | None,
    params: QuadratDetectionParams,
) -> QuadratDetectionResult:
    """Process the image and return it."""
    if not image_path:
        return QuadratDetectionResult(None, None, None)

    original_img = _read_image(image_path)
    if original_img is None:
        return QuadratDetectionResult(None, None, None)

    if params.downscale.enabled:
        original_img = _downscale_image(original_img, params.downscale)

    img = _grayscale_image(original_img)

    # Create transparent empty image
    debug_img = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)

    if params.blur.enabled:
        img = _blur_image(img, params.blur)

    if params.thresholding.method != ThresholdingMethod.NONE:
        img = _threshold_image(img, params.thresholding)

    if params.canny.enabled:
        img = _canny_image(img, params.canny)

    if params.hough.enabled:
        (debug_img, lines) = _hough(img, debug_img, params.hough)
        corners = _find_corners(lines, debug_img)
        logger.debug(f"Detected corners: {corners}")

    if params.findContour.enabled:
        debug_img = _find_contours(img, debug_img, params.findContour)

    return QuadratDetectionResult(original_img, img, debug_img)


def _read_image(image_path: str) -> MatLike | None:
    """Read the image from the given path."""
    logger.debug(f"Reading image {image_path}...")
    img = cv2.imread(image_path, cv2.IMREAD_COLOR_BGR)
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

    threshold_type: int | None = None
    if method == ThresholdingMethod.BINARY:
        threshold_type = cv2.THRESH_BINARY_INV if params.inverse else cv2.THRESH_BINARY
    elif method == ThresholdingMethod.TRUNC:
        threshold_type = cv2.THRESH_TRUNC
    elif method == ThresholdingMethod.TO_ZERO:
        threshold_type = cv2.THRESH_TOZERO_INV if params.inverse else cv2.THRESH_TOZERO

    if threshold_type is not None:
        if params.otsu_enabled:
            # Thresholding with Otsu's method ignores the given threshold value
            threshold_type |= cv2.THRESH_OTSU
        # Thresholding with anything other than BINARY or BINARY_INV ignores the maximum value
        _, img = cv2.threshold(img, threshold, maximum, threshold_type)
    else:
        threshold_type = cv2.THRESH_BINARY_INV if params.inverse else cv2.THRESH_BINARY

        if method == ThresholdingMethod.MEAN:
            img = cv2.adaptiveThreshold(img, maximum, cv2.ADAPTIVE_THRESH_MEAN_C, threshold_type, block_size, C)
        elif method == ThresholdingMethod.GAUSSIAN:
            img = cv2.adaptiveThreshold(img, maximum, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, threshold_type, block_size, C)
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


@dataclass
class Line:
    rho: float
    theta: float  # radians


def _hough(img: MatLike, debug_img: MatLike, params: HoughParams) -> tuple[MatLike, list[Line]]:
    """Apply Hough Transform to detect lines in the image."""
    logger.debug("Applying Hough Transform...")

    result: list[Line] = []
    rho: float
    theta: float

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
                # Convert to (rho, theta)
                a = x2 - x1
                b = y2 - y1
                theta = math.atan2(b, a)
                rho = x1 * math.cos(theta) + y1 * math.sin(theta)
                result.append(Line(rho, theta))
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
                result.append(Line(rho, theta))
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
                pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))
                cv2.line(debug_img, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            logger.debug("No lines found.")

    return (debug_img, result)


def _find_corners(lines: list[Line], debug_img: MatLike) -> list[tuple[int, int]]:
    """Find corners from the detected lines."""
    logger.debug("Finding corners from lines...")
    corners: list[tuple[int, int]] = []
    angle_threshold = math.radians(20)  # minimum angle difference to consider lines non-parallel
    height, width = debug_img.shape[:2]

    def intersection(line1: Line, line2: Line) -> tuple[int, int] | None:
        # Solve for intersection of two lines in (rho, theta) form
        # Line: x*cos(theta) + y*sin(theta) = rho
        a1, b1, c1 = math.cos(line1.theta), math.sin(line1.theta), line1.rho
        a2, b2, c2 = math.cos(line2.theta), math.sin(line2.theta), line2.rho
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-10:
            return None
        x = (b2 * c1 - b1 * c2) / det
        y = (a1 * c2 - a2 * c1) / det
        return (int(round(x)), int(round(y)))

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            theta1 = lines[i].theta
            theta2 = lines[j].theta
            angle_diff = abs((theta1 - theta2) % math.pi)
            # angle_diff = abs((theta1 - theta2 + math.pi) % math.pi - math.pi/2)
            if angle_diff < angle_threshold:
                continue  # skip nearly parallel lines
            pt = intersection(lines[i], lines[j])
            if pt is not None:
                x, y = pt
                if 0 <= x < width and 0 <= y < height:
                    corners.append(pt)
                    cv2.circle(debug_img, pt, 3, (255, 0, 0, 255), -1)
    logger.debug(f"Found {len(corners)} corners.")
    return corners


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
