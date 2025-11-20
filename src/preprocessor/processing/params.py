from dataclasses import dataclass
from enum import Enum


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
class QuadratDetectionParams:
    downscale: DownscaleParams
    blur: BlurParams
    thresholding: ThresholdingParams
    canny: CannyParams
    hough: HoughParams
    findContour: FindContourParams


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
        threshold=225,
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
        enabled=False,
        probabilistic=False,
        rho=1,
        theta=2,  # degrees
        threshold=50,
        srn=0.0,
        stn=0.0,
        min_theta=0.0,
        max_theta=180.0,
        min_line_length=50,
        max_line_gap=10,
    ),
    findContour=FindContourParams(
        enabled=False,
        method=ContourApproximationMethod.SIMPLE,
    ),
)
