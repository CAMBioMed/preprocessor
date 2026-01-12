# from typing import TypeVar, Sequence

from cv2.typing import Point2f

from preprocessor.processing.detect_quadrat import QuadratDetectionResult


# T = TypeVar("T")
#
# def _serialize_sequence(seq: Sequence[T]) -> list[T]:
#     """Convert a sequence (including NumPy arrays/scalars) to a plain Python list of floats."""
#     row: list[T] = []
#     for v in seq:
#         row.append(v)
#     return row

def serialize_photo_metadata(result: QuadratDetectionResult, quality: int = 95) -> dict:
    corners = None if result.corners is None else [_serialize_point2f(pt) for pt in result.corners]
    return {
        "quality": quality,
        "detection": {
            "corners": corners,
        }
    }


def _serialize_point2f(pt: Point2f) -> list[float]:
    """Convert a Point2f to a plain Python list of floats."""
    return [float(pt[0]), float(pt[1])]


def _deserialize_point2f(data: list[float]) -> Point2f:
    """Convert a plain Python list of floats to a Point2f."""
    if not isinstance(data, (list, tuple)):
        raise ValueError("data must be a list or tuple of two numeric values")
    if len(data) != 2:
        raise ValueError("data must contain exactly two elements for a Point2f")
    try:
        x = float(data[0])
        y = float(data[1])
    except Exception as exc:
        raise ValueError("elements of data must be convertible to float") from exc
    return x, y