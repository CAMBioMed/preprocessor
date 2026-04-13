import pytest

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, ClassVar

from preprocessor.core.model import MetadataData


# Make this base test generic over the pydantic model type being tested.
ModelT = TypeVar("ModelT", bound=MetadataData)


class ModelBaseTest(ABC, Generic[ModelT]):
    fields_and_values: ClassVar[dict[str, tuple[
        object | None,
        list[object],
        list[tuple[object, object]],
        list[object],
    ]]]
    """Subclasses must provide this mapping. For each field name the tuple contains:
    - the default value,
    - a list of valid values,
    - a list of pairs: unnormalized value to normalized value,
    - a list of invalid values
    """

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        # Ensure subclass provided the required mapping as a class attribute
        if "fields_and_values" not in cls.__dict__:
            raise TypeError("Subclasses of ModelBaseTest must define a class-level 'fields_and_values' mapping")

    @abstractmethod
    def create_model(self) -> ModelT:
        """Return an empty/new instance of the model under test."""

    @abstractmethod
    def update_model(self, model: ModelT, field_name: str, new_value: object) -> ModelT:
        """Updates the specified field of the specified model and returns the new model
        (or the same model if the update was in-place). Implementations are responsible
        for performing validation as the concrete model would."""

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
        """Model properties can be set to a valid value."""
        # Arrange: empty model
        model = self.create_model()

        # Assert: the initial value is as expected
        actual_value = getattr(model, field_name)
        assert actual_value == initial_value, \
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"

        # Act: update the model
        new_model = self.update_model(model, field_name, new_value)

        # Assert: the value is updated
        actual_value = getattr(new_model, field_name)
        assert actual_value == new_value, \
            f"After setting, value of {field_name} should be {new_value}, but got {actual_value}"

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
        """Model properties should enforce type validation and constraints when set."""
        # Arrange: empty model
        model = self.create_model()

        # Assert: the initial value is as expected
        actual_value = getattr(model, field_name)
        assert actual_value == initial_value, \
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"

        # Assert: updating the model with an invalid value should fail
        with pytest.raises(ValueError):
            self.update_model(model, field_name, invalid_value)

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
        """Model properties should normalize (trimming, empty to None) on assignment."""
        # Arrange: empty model
        model = self.create_model()

        # Assert: the initial value is as expected
        actual_value = getattr(model, field_name)
        assert actual_value == initial_value, \
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"

        # Act: set the value
        new_model = self.update_model(model, field_name, input_value)

        # Assert: the value is normalized as expected
        assert getattr(new_model, field_name) == expected_value
