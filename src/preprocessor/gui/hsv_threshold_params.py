from dataclasses import dataclass


@dataclass
class HSVThresholdParams:
    hue_min: int
    hue_max: int
    saturation_min: int
    saturation_max: int
    value_min: int
    value_max: int

    def __post__init__(self) -> None:
        # Validation
        assert 0 <= self.hue_min <= 255, "hue_min must be in the range [0, 255]"
        assert 0 <= self.hue_max <= 255, "hue_max must be in the range [0, 255]"
        assert 0 <= self.saturation_min <= 255, "saturation_min must be in the range [0, 255]"
        assert 0 <= self.saturation_max <= 255, "saturation_max must be in the range [0, 255]"
        assert 0 <= self.value_min <= 255, "value_min must be in the range [0, 255]"
        assert 0 <= self.value_max <= 255, "value_max must be in the range [0, 255]"

        # Adjustment
        # FIXME: Adjustment doesn't work because it gets overwritten immediately after by replace()
        new_hue_min = min(self.hue_min, self.hue_max)
        new_hue_max = max(self.hue_min, self.hue_max)
        self.hue_min = new_hue_min
        self.hue_max = new_hue_max
        new_saturation_min = min(self.saturation_min, self.saturation_max)
        new_saturation_max = max(self.saturation_min, self.saturation_max)
        self.saturation_min = new_saturation_min
        self.saturation_max = new_saturation_max
        new_value_min = min(self.value_min, self.value_max)
        new_value_max = max(self.value_min, self.value_max)
        self.value_min = new_value_min
        self.value_max = new_value_max
