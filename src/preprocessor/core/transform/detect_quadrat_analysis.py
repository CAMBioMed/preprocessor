from abc import ABC
from typing import overload, override

from preprocessor.core.message_reporter import MessageReporter, NOOP_MESSAGE_REPORTER
from preprocessor.core.progress_reporter import ProgressReporter, NOOP_PROGRESS_REPORTER
from preprocessor.core.type_corners import Corners
from preprocessor.core.types import ImageRGB, Line, Point2D
from preprocessor.gui.jobs.qjobs import CancelToken
import logging
import math
from dataclasses import dataclass
from dataclasses import dataclass
from enum import Enum

import cv2
import numpy as np
from cv2.typing import MatLike, Point2f
from sklearn.cluster import KMeans


logger = logging.getLogger(__name__)

class ThresholdingMethod(Enum):
    NONE = "None"
    BINARY = "Binary"
    TRUNC = "Truncate"
    TO_ZERO = "To Zero"
    MEAN = "Mean"
    GAUSSIAN = "Gaussian"

    @staticmethod
    def from_string(method_name: str) -> "ThresholdingMethod":
        for method in ThresholdingMethod:
            if method.value == method_name:
                return method
        msg = f"Unknown ThresholdingMethod: {method_name}"
        raise NotImplementedError(msg)


class ContourApproximationMethod(Enum):
    NONE = "None"
    SIMPLE = "Simple"
    TC89_L1 = "Teh-Chin L1"
    TC89_KCOS = "Teh-Chin KCOS"

    @staticmethod
    def from_string(method_name: str) -> "ContourApproximationMethod":
        for method in ContourApproximationMethod:
            if method.value == method_name:
                return method
        msg = f"Unknown ContourApproximationMethod: {method_name}"
        raise NotImplementedError(msg)


@dataclass
class DownscaleParams:
    enabled: bool
    max_size: int


@dataclass
class BlurParams:
    enabled: bool
    kernel_size: int


@dataclass
class ThresholdingParams:
    method: ThresholdingMethod
    inverse: bool
    threshold: int
    maximum: int
    block_size: int
    C: float
    otsu_enabled: bool


@dataclass
class CannyParams:
    enabled: bool
    threshold1: int
    threshold2: int
    aperture_size: int


@dataclass
class HoughParams:
    enabled: bool
    probabilistic: bool
    rho: int  # px
    theta: float  # degrees
    threshold: int  # votes
    srn: float
    stn: float
    min_theta: float  # degrees
    max_theta: float  # degrees
    min_line_length: int  # px
    max_line_gap: int  # px


@dataclass
class FindContourParams:
    enabled: bool
    method: ContourApproximationMethod


@dataclass
class FixPerspectiveParams:
    enabled: bool
    target_width: int
    target_height: int


@dataclass
class QuadratDetectionParams:
    downscale: DownscaleParams
    blur: BlurParams
    thresholding: ThresholdingParams
    canny: CannyParams
    hough: HoughParams
    find_contour: FindContourParams
    fix_perspective: FixPerspectiveParams


defaultParams: QuadratDetectionParams = QuadratDetectionParams(
    downscale=DownscaleParams(
        enabled=True,
        max_size=400,
    ),
    blur=BlurParams(
        enabled=True,
        kernel_size=5,
    ),
    thresholding=ThresholdingParams(
        method=ThresholdingMethod.BINARY,
        inverse=False,
        threshold=190,
        maximum=255,
        block_size=3,
        C=1.0,
        otsu_enabled=False,
    ),
    canny=CannyParams(
        enabled=True,
        threshold1=50,
        threshold2=150,
        aperture_size=5,
    ),
    hough=HoughParams(
        enabled=True,
        probabilistic=False,
        rho=1,
        theta=3,  # degrees
        threshold=65,
        srn=0.0,
        stn=0.0,
        min_theta=0.0,
        max_theta=180.0,
        min_line_length=50,
        max_line_gap=10,
    ),
    find_contour=FindContourParams(
        enabled=False,
        method=ContourApproximationMethod.SIMPLE,
    ),
    fix_perspective=FixPerspectiveParams(
        enabled=True,
        target_width=1024,
        target_height=1024,
    ),
)

    
class DetectQuadratAnalysisJob():
    """Detect quadrat corners from an image using the specified parameters."""

    name: str = "Detect Quadrat Analysis"
    _image: ImageRGB
    _params: QuadratDetectionParams

    def __init__(
        self,
        image: ImageRGB,
        params: QuadratDetectionParams,
    ) -> None:
        self._image = image
        self._params = params

    # @override
    def __call__(
        self,
        cancel_token: CancelToken = CancelToken(),
        messages: MessageReporter = NOOP_MESSAGE_REPORTER,
        progress: ProgressReporter = NOOP_PROGRESS_REPORTER,
    ) -> Corners:
        params = self._params
        original_img = self._image.data.copy()

        if params.downscale.enabled:
            original_img, scale = DetectQuadratAnalysisJob._downscale_image(original_img, params.downscale)
        else:
            scale = 1.0

        img = DetectQuadratAnalysisJob._grayscale_image(original_img)

        if params.blur.enabled:
            img = DetectQuadratAnalysisJob._blur_image(img, params.blur)

        if params.thresholding.method != ThresholdingMethod.NONE:
            img = DetectQuadratAnalysisJob._threshold_image(img, params.thresholding)

        if params.canny.enabled:
            img = DetectQuadratAnalysisJob._canny_image(img, params.canny)

        # Create copy of processed image
        debug_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        corners: list[Point2D] = []
        if params.hough.enabled:
            (debug_img, lines) = DetectQuadratAnalysisJob._hough(img, debug_img, params.hough)
            corners = DetectQuadratAnalysisJob._find_corners(lines, debug_img, scale)
            logger.debug(f"Detected corners: {corners}")

        if params.find_contour.enabled:
            debug_img = DetectQuadratAnalysisJob._find_contours(img, debug_img, params.find_contour)

        return Corners(tuple(corners))

    @staticmethod
    def _downscale_image(img: MatLike, params: DownscaleParams) -> tuple[MatLike, float]:
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
                return img, scale
        except Exception:
            # if resizing fails for any reason, continue with original image
            pass
        return img, 1.0

    @staticmethod
    def _grayscale_image(img: MatLike) -> MatLike:
        """Convert the image to grayscale."""
        logger.debug("Graying image...")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        logger.debug("Grayed image.")
        return img

    @staticmethod
    def _blur_image(img: MatLike, params: BlurParams) -> MatLike:
        """Blur the image with the given kernel size."""
        logger.debug("Blurring image...")
        img = cv2.GaussianBlur(img, (params.kernel_size, params.kernel_size), 0)
        logger.debug("Blurred image")
        return img

    @staticmethod
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

    @staticmethod
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


    @staticmethod
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

    @staticmethod
    def _find_corners(
        lines: list[Line],
        debug_img: MatLike,
        scale: float = 1.0,
        draw_debug: bool = True,
    ) -> list[Point2D]:
        """Find corners from the detected lines."""
        logger.debug("Finding corners from lines...")
        corners: list[Point2D] = []
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
            return round(x), round(y)

        def angle_difference(theta1: float, theta2: float) -> float:
            a = theta1 % math.pi
            b = theta2 % math.pi
            diff = abs(a - b)
            return min(diff, math.pi - diff)

        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                theta1 = lines[i].theta
                theta2 = lines[j].theta
                angle_diff = angle_difference(theta1, theta2)
                if angle_diff < angle_threshold:
                    continue  # skip nearly parallel lines
                pt = intersection(lines[i], lines[j])
                if pt is not None:
                    x, y = pt
                    if 0 <= x < width and 0 <= y < height:
                        corners.append(pt)
                        cv2.circle(debug_img, pt, 2, (255, 0, 0, 255), -1)
        logger.debug(f"Found {len(corners)} candidate corners.")
        if not corners:
            return []

        points = np.array(corners)  # shape (N,2)

        # Compute the centroid of the corners
        centroid = points.mean(axis=0)

        # Convert points to angles around the centroid
        vecs = points - centroid
        angles = np.arctan2(vecs[:, 1], vecs[:, 0])  # range [-pi, pi]

        # Cluster by angles into 4 quadrants
        circle_coords = np.column_stack([np.cos(angles), np.sin(angles)])
        kmeans = KMeans(n_clusters=4, n_init="auto").fit(circle_coords)
        labels = kmeans.labels_

        # For each cluster, pick the points closes to the centroid
        corner_points = []
        for c in range(4):
            group = points[labels == c]
            dists = np.linalg.norm(group - centroid, axis=1)
            if dists.size == 0:
                continue
            corner_points.append(group[np.argmin(dists)])

        if len(corner_points) < 4:
            logger.debug("Could not find 4 distinct corners.")
            return []

        # Order the points clockwise starting from top-left
        corner_points_np = np.array(corner_points)
        # sort by y
        top, bottom = (
            corner_points_np[corner_points_np[:, 1].argsort()][:2],
            corner_points_np[corner_points_np[:, 1].argsort()][2:],
        )
        # sort each pair by x
        tl, tr = top[top[:, 0].argsort()]
        bl, br = bottom[bottom[:, 0].argsort()]
        ordered_corners = np.array([tl, tr, br, bl])  # Clockwise from the top-left

        for c in ordered_corners:
            cv2.circle(debug_img, (c[0], c[1]), 2, (0, 255, 0, 255), -1)

        def to_tuple(p: np.ndarray) -> tuple[int, int]:
            return int(p[0]), int(p[1])

        if draw_debug and len(ordered_corners) > 1:
            for i in range(len(ordered_corners)):
                pt1 = (int(ordered_corners[i][0]), int(ordered_corners[i][1]))
                pt2 = (int(ordered_corners[(i + 1) % 4][0]), int(ordered_corners[(i + 1) % 4][1]))
                cv2.line(debug_img, pt1, pt2, (255, 0, 255), 2, cv2.LINE_AA)

        # Scale all corners back to original image size
        unscaled_corners = ordered_corners / scale

        return list(map(to_tuple, unscaled_corners))

    @staticmethod
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
