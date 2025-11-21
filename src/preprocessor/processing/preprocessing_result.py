from dataclasses import dataclass

from cv2.typing import MatLike


@dataclass
class AbstractResult:
    final: MatLike | None
    debug: MatLike | None = None


@dataclass
class OriginalResult(AbstractResult):
    final: MatLike | None
    debug: None = None

@dataclass
class LensCorrectedResult(AbstractResult):
    final: MatLike | None
    debug: MatLike | None = None

@dataclass
class ColorCorrectedResult(AbstractResult):
    final: MatLike | None
    debug: MatLike | None = None

@dataclass
class PerspectiveCorrectedResult(AbstractResult):
    final: MatLike | None
    debug: MatLike | None = None
    processed: MatLike | None = None


@dataclass
class PreprocessingResult:
    original: OriginalResult
    lens_corrected: LensCorrectedResult
    color_corrected: ColorCorrectedResult
    perspective_corrected: PerspectiveCorrectedResult
