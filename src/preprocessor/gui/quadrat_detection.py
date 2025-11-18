from dataclasses import dataclass
from enum import Enum

class ThresholdingMethod(Enum):
    NONE = 'None'
    BINARY = 'Binary'
    BINARY_INV = 'Binary Inverse'
    TRUNC = 'Truncate'
    TOZERO = 'To Zero'
    TOZERO_INV = 'To Zero Inverse'
    MEAN = 'Mean'
    GAUSSIAN = 'Gaussian'

@dataclass
class QuadratDetectionParams:
    downscale_enabled: bool
    downscale_max_size: int
    blur_enabled: bool
    blur_kernel_size: int
    thresholding_method: ThresholdingMethod
    thresholding_threshold: int
    thresholding_maximum: int
    thresholding_block_size: int
    thresholding_C: int
    thresholding_otsu_enabled: bool
    canny_enabled: bool
    canny_threshold1: int
    canny_threshold2: int
    canny_aperture_size: int
