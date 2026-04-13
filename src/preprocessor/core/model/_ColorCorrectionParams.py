from pydantic import BaseModel, ConfigDict


class ColorCorrectionParams(BaseModel, validate_assignment=True):
    """Parameters for color correction."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    # TODO: To be replaced
    gain_r: float = 1.0
    gain_g: float = 1.0
    gain_b: float = 1.0

    # TODO: Implement validation

