from dataclasses import dataclass
from enum import Enum


class ThresholdingMethod(Enum):
    NONE = "None"
    BINARY = "Binary"
    BINARY_INV = "Binary Inverse"
    TRUNC = "Truncate"
    TOZERO = "To Zero"
    TOZERO_INV = "To Zero Inverse"
    MEAN = "Mean"
    GAUSSIAN = "Gaussian"

    @staticmethod
    def from_string(method_name: str) -> "ThresholdingMethod":
        for method in ThresholdingMethod:
            if method.value == method_name:
                return method
        msg = f"Unknown ThresholdingMethod: {method_name}"
        raise NotImplementedError(msg)


@dataclass
class QuadratDetectionParams:
    # Downscale
    downscale_enabled: bool
    downscale_max_size: int
    # Blur
    blur_enabled: bool
    blur_kernel_size: int
    # Thresholding
    thresholding_method: ThresholdingMethod
    thresholding_threshold: int
    thresholding_maximum: int
    thresholding_block_size: int
    thresholding_C: float
    thresholding_otsu_enabled: bool
    # Canny
    canny_enabled: bool
    canny_threshold1: int
    canny_threshold2: int
    canny_aperture_size: int


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
