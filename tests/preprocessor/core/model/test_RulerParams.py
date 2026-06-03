from typing import override, ClassVar

import pytest

from preprocessor.core.model import LensCorrectionParams, RulerParams
from preprocessor.core.type_corners import Corners
from tests.preprocessor.core.model.cls_PydanticModelTestBase import PydanticModelTestBase


class Test_RulerParams(PydanticModelTestBase):
    fields_and_values: ClassVar[
        dict[
            str,
            tuple[
                object | None,
                list[object],
                list[tuple[object, object]],
                list[object],
            ],
        ]
    ] = {
        "start": (
            # Initial
            None,
            # Valid
            [
                (0.0, 0.0),
                (5.0, 8.0),
            ],
            # Normalized
            [],
            # Invalid
            [
                "foo",  # Not a Point2D instance
            ],
        ),
        "end": (
            # Initial
            None,
            # Valid
            [
                (0.0, 0.0),
                (7.0, 9.0),
            ],
            # Normalized
            [],
            # Invalid
            [
                "foo",  # Not a Point2D instance
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
    def create_model(self) -> RulerParams:
        return RulerParams()

    @override
    def update_model(self, model: RulerParams, field_name: str, new_value: object) -> RulerParams:
        # We cannot use model_copy() here because it doesn't validate
        new_model = RulerParams.model_validate({**model.model_dump(), field_name: new_value})
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
