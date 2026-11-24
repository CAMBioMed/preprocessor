"""Validated type aliases for serialized lens-correction parameters."""

from pydantic import FiniteFloat

type LensVector = list[FiniteFloat]
"""A list of finite distortion coefficients used for lens correction."""

type Matrix3x3 = tuple[
    tuple[FiniteFloat, FiniteFloat, FiniteFloat],
    tuple[FiniteFloat, FiniteFloat, FiniteFloat],
    tuple[FiniteFloat, FiniteFloat, FiniteFloat],
]
"""A finite 3x3 camera intrinsic matrix used for lens correction."""
