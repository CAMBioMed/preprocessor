from cv2.typing import MatLike

from preprocessor.model import Matrix3x3


def apply_distortion(
    img: MatLike,
    camera_matrix: Matrix3x3,
    dist_coeffs: list[float],
) -> MatLike:
    """Correct lens distortion in the given image using the specified parameters."""
    import cv2
    import numpy as np

    h, w = img.shape[:2]
    np_camera_matrix = np.array(camera_matrix, dtype=np.float32)
    np_dist_coeffs = np.array(dist_coeffs, dtype=np.float32)

    # Compute the optimal new camera matrix to minimize distortion
    new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(np_camera_matrix, np_dist_coeffs, (w, h), 1)

    # Undistort the image using the computed camera matrix and distortion coefficients
    undistorted_img = cv2.undistort(img, np_camera_matrix, np_dist_coeffs, None, new_camera_matrix)

    return undistorted_img