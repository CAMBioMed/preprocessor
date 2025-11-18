from dataclasses import dataclass


@dataclass
class QuadratDetectionParams:
    downscale_enabled: bool
    downscale_max_size: int
    blur_enabled: bool
    blur_kernel_size: int
    canny_enabled: bool
    canny_threshold1: int
    canny_threshold2: int
    canny_aperture_size: int