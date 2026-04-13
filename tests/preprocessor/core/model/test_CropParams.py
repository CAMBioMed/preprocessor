from typing import override

import pytest

from preprocessor.core.model import LensCorrectionParams, CropParams
from preprocessor.core.type_corners import Corners
from tests.preprocessor.core.model.cls_ModelTestBase import ModelBaseTest


class Test_CropParams(ModelBaseTest):


    fields_and_values: dict[str, tuple[
        object | None,
        list[object],
        list[tuple[object, object]],
        list[object],
    ]] = {
        "corners": (
            # Initial
            Corners(()),
            # Valid
            [
                Corners(((0.1, 0.2), (1.1, 0.2), (1.1, 1.2), (0.1, 1.2))),
            ],
            # Normalized
            [],
            # Invalid
            [
                "foo",  # Not a Corners instance
                None,  # None is not a valid value for corners
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
    def create_model(self) -> CropParams:
        return CropParams()

    @override
    def update_model(self, model: CropParams, field_name: str, new_value: object) -> CropParams:
        # We cannot use model_copy() here because it doesn't validate
        new_model = CropParams.model_validate({**model.model_dump(), field_name: new_value})
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
