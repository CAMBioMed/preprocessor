from typing import override, ClassVar

import pytest

from preprocessor.core.model import LensCorrectionParams
from tests.preprocessor.core.model.cls_PydanticModelTestBase import PydanticModelTestBase


class Test_LensCorrectionParams(PydanticModelTestBase):

    fields_and_values: ClassVar[dict[str, tuple[
        object | None,
        list[object],
        list[tuple[object, object]],
        list[object],
    ]]] = {
        "camera_matrix": (
            # Initial
            None,
            # Valid
            [
                ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, 1.0)),
            ],
            # Normalized
            [],
            # Invalid
            [
                "foo",
                ((1000.0, 0.0), (0.0, 1000.0)),
            ],
        ),
        "coefficients": (
            # Initial
            None,
            # Valid
            [
                [0.01, -0.02, 0.001, 0.0005],
                [0.4] * 4,
                [0.5] * 5,
                [0.8] * 8,
                [0.12] * 12,
                [0.14] * 14,
            ],
            # Normalized
            [],
            # Invalid
            [
                "foo",  # Not a list
                [0.01, -0.02],  # Too few items (min 4)
                [0.01] * 15,  # Too many items (max 14)
                [0.01, float("nan"), 0.0, 0.0],  # NaN is not allowed in coefficients
            ],
        ),
    }
    """Map for each field name to:
        - the default value,
        - a list of valid values,
        - a list of pairs: unnormalized value to normalized value,
        - a list of invalid values
        """

    @override
    def create_model(self) -> LensCorrectionParams:
        return LensCorrectionParams()

    @override
    def update_model(self, model: LensCorrectionParams, field_name: str, new_value: object) -> LensCorrectionParams:
        # We cannot use model_copy() here because it doesn't validate
        new_model = LensCorrectionParams.model_validate({**model.model_dump(), field_name: new_value})
        return new_model

    @pytest.mark.parametrize(
        "field_name, initial_value, new_value",
        [(n, v, vv) for n, (v, vvs, _, _) in fields_and_values.items() for vv in vvs],
    )
    def test_property_valid_value(
            self,
            field_name: str,
            initial_value: object,
            new_value: object,
    ) -> None:
        self.assert_property_valid_value(field_name, initial_value, new_value)

    @pytest.mark.parametrize(
        "field_name, initial_value, invalid_value",
        [(n, v, iv) for n, (v, _, _, ivs) in fields_and_values.items() for iv in ivs],
    )
    def test_property_invalid_value(
            self,
            field_name: str,
            initial_value: object,
            invalid_value: object,
    ) -> None:
        self.assert_property_invalid_value(field_name, initial_value, invalid_value)

    @pytest.mark.parametrize(
        "field_name, initial_value, input_value, expected_value",
        [(n, v, lv, rv) for n, (v, _, nvs, _) in fields_and_values.items() for (lv, rv) in nvs],
    )
    def test_property_normalization(
            self,
            field_name: str,
            initial_value: object,
            input_value: object,
            expected_value: object,
    ) -> None:
        self.assert_property_normalization(field_name, initial_value, input_value, expected_value)
