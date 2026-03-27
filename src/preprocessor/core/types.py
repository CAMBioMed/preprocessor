import numpy as np
import numpy.typing as npt

Point2D = tuple[float, float]
"""A 2D point represented as a tuple of (x, y) coordinates."""

Image = npt.NDArray[np.number]
"""Defines the Image type as a numpy array with a numeric dtype (integer or floating),
and with 2 or 3 dimensions (grayscale or color).

This is also an OpenCV2 MatLike."""

LensVector = list[float]
"""Defines the LensVector type as a list of floats, representing distortion coefficients for lens correction."""

# def require_is_image(obj: object) -> None:
#     """Helper function to check if an object is a valid Image, and raise a TypeError if not."""
#     if not isinstance(obj, np.ndarray):
#         raise TypeError(f"Expected numpy.ndarray, got {type(obj)!r}")
#     if obj.ndim not in (2, 3):
#         raise ValueError(f"Expected 2D (grayscale) or 3D (color) array, got ndim={obj.ndim}")
#     if obj.size == 0:
#         raise ValueError("Empty image array")

