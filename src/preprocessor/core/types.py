from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
import numpy.typing as npt

Point2D = tuple[float, float]
"""A 2D point represented as a tuple of (x, y) coordinates."""

@dataclass
class Line:
    rho: float
    theta: float  # radians

ImageArray = npt.NDArray[np.uint8]
"""Defines the Image type as a numpy array of 8-bit integers,
and with 2 or 3 dimensions (grayscale or color).

This is also an OpenCV2 MatLike."""

LensVector = list[float]
"""Defines the LensVector type as a list of floats, representing distortion coefficients for lens correction."""

# TODO: Rename to Matrix3x3
CameraMatrix = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]
"""Defines the CameraMatrix type as a 3x3 tuple of floats,
representing the camera intrinsic matrix for lens correction."""


@dataclass(frozen=True)
class ImageRGB:
    """Wrapper for an RGB image."""

    data: ImageArray

    def __post_init__(self) -> None:
        if not isinstance(self.data, np.ndarray):
            msg = "Data must be a numpy.ndarray"
            raise TypeError(msg)
        if self.data.dtype != np.uint8:
            msg = f"Expected dtype np.uint8, got {self.data.dtype!r}"
            raise TypeError(msg)
        nd = self.data.ndim
        if nd != 3 or self.data.shape[2] != 3:
            msg = "RGB image must be HxWx3"
            raise ValueError(msg)
        if self.data.size == 0:
            msg = "Empty image array"
            raise ValueError(msg)

    @classmethod
    def from_file(cls, path: Path) -> "ImageRGB":
        """Load an image from a file path and return an ImageRGB instance.

        :param path: The file path to load the image from.
        :return: An ImageRGB instance containing the loaded image data.
        :raises ValueError: If loading the image fails.
        """
        arr = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if arr is None:
            msg = f"Failed to load image from {path!s}"
            raise ValueError(msg)
        rgb_arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
        return cls.from_rgb_array(rgb_arr)

    def to_file(self, path: Path, quality: float = 0.95) -> None:
        """Save the image to a file path.

        :param path: The file path to save the image to.
        :param quality: The JPEG quality (0.0-1.0) to use when saving the image.
        :raises ValueError: If saving the image fails.
        """
        return self.to_bgr_image().to_file(path, quality=quality)

    @classmethod
    def from_rgb_array(cls, arr: npt.ArrayLike) -> "ImageRGB":
        """Create an ImageRGB from an array-like, validating and casting it to np.uint8."""
        arr = np.asarray(arr)
        return cls(data=arr.astype(np.uint8, copy=False))

    def to_bgr_image(self) -> "ImageBGR":
        return ImageBGR.from_bgr_array(cv2.cvtColor(self.data, cv2.COLOR_RGB2BGR))

    def to_rgb_image(self) -> "ImageRGB":
        return self

    def to_grayscale_image(self) -> "ImageGreyscale":
        return ImageGreyscale.from_greyscale_array(cv2.cvtColor(self.data, cv2.COLOR_RGB2GRAY))


@dataclass(frozen=True)
class ImageBGR:
    """Wrapper for a BGR image."""

    data: ImageArray

    def __post_init__(self) -> None:
        if not isinstance(self.data, np.ndarray):
            msg = "Data must be a numpy.ndarray"
            raise TypeError(msg)
        if self.data.dtype != np.uint8:
            msg = f"Expected dtype np.uint8, got {self.data.dtype!r}"
            raise TypeError(msg)
        nd = self.data.ndim
        if nd != 3 or self.data.shape[2] != 3:
            msg = "BGR image must be HxWx3"
            raise ValueError(msg)
        if self.data.size == 0:
            msg = "Empty image array"
            raise ValueError(msg)

    @classmethod
    def from_file(cls, path: Path) -> "ImageBGR":
        """Load an image from a file path and return an ImageBGR instance.

        :param path: The file path to load the image from.
        :return: An ImageRGB instance containing the loaded image data.
        :raises ValueError: If loading the image fails.
        """
        arr = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if arr is None:
            msg = f"Failed to load image from {path!s}"
            raise ValueError(msg)
        return cls.from_bgr_array(arr)

    def to_file(self, path: Path, quality: float = 0.95) -> None:
        """Save the image to a file path.

        :param path: The file path to save the image to.
        :param quality: The JPEG quality (0.0-1.0) to use when saving the image.
        :raises ValueError: If saving the image fails.
        """
        bgr_arr = self.data
        params = [cv2.IMWRITE_JPEG_QUALITY, round(quality * 100)]
        success = cv2.imwrite(str(path), bgr_arr, params)
        if not success:
            msg = f"Failed to save image to {path!s}"
            raise ValueError(msg)

    @classmethod
    def from_bgr_array(cls, arr: npt.ArrayLike) -> "ImageBGR":
        """Create an ImageBGR from an array-like, validating and casting it to np.uint8."""
        arr = np.asarray(arr)
        return cls(data=arr.astype(np.uint8, copy=False))

    def to_bgr_image(self) -> "ImageBGR":
        return self

    def to_rgb_image(self) -> ImageRGB:
        return ImageRGB.from_rgb_array(cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB))

    def to_grayscale_image(self) -> "ImageGreyscale":
        return ImageGreyscale.from_greyscale_array(cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY))


@dataclass(frozen=True)
class ImageGreyscale:
    """Wrapper for a greyscale image."""

    data: ImageArray

    def __post_init__(self) -> None:
        if not isinstance(self.data, np.ndarray):
            msg = "Data must be a numpy.ndarray"
            raise TypeError(msg)
        if self.data.dtype != np.uint8:
            msg = f"Expected dtype np.uint8, got {self.data.dtype!r}"
            raise TypeError(msg)
        nd = self.data.ndim
        # Accept either a 2D array (H, W) or a 3D array with a singleton channel (H, W, 1)
        if not (nd == 2 or (nd == 3 and self.data.shape[2] == 1)):
            msg = "Greyscale image must be HxW or HxWx1"
            raise ValueError(msg)
        if self.data.size == 0:
            msg = "Empty image array"
            raise ValueError(msg)

    @classmethod
    def from_file(cls, path: Path) -> "ImageGreyscale":
        """Load an image from a file path and return an ImageGreyscale instance.

        :param path: The file path to load the image from.
        :return: An ImageRGB instance containing the loaded image data.
        :raises ValueError: If loading the image fails.
        """
        arr = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if arr is None:
            msg = f"Failed to load image from {path!s}"
            raise ValueError(msg)
        return cls.from_greyscale_array(arr)

    def to_file(self, path: Path, quality: float = 0.95) -> None:
        """Save the image to a file path.

        :param path: The file path to save the image to.
        :param quality: The JPEG quality (0.0-1.0) to use when saving the image.
        :raises ValueError: If saving the image fails.
        """
        return self.to_bgr_image().to_file(path, quality=quality)

    @classmethod
    def from_greyscale_array(cls, arr: npt.ArrayLike) -> "ImageGreyscale":
        """Create an ImageGreyscale from an array-like, validating and casting it to np.uint8."""
        arr = np.asarray(arr)
        return cls(data=arr.astype(np.uint8, copy=False))

    def to_bgr_image(self) -> ImageBGR:
        return ImageBGR.from_bgr_array(cv2.cvtColor(self.data, cv2.COLOR_GRAY2BGR))

    def to_rgb_image(self) -> ImageRGB:
        return ImageRGB.from_rgb_array(cv2.cvtColor(self.data, cv2.COLOR_GRAY2RGB))

    def to_grayscale_image(self) -> "ImageGreyscale":
        return self
