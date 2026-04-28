import pytest

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, ClassVar

from pydantic import BaseModel


# Make this base test generic over the pydantic model type being tested.
ModelT = TypeVar("ModelT", bound=BaseModel)


class PydanticModelTestBase(ABC, Generic[ModelT]):
    @abstractmethod
    def create_model(self) -> ModelT:
        """Return an empty/new instance of the model under test."""

    @abstractmethod
    def update_model(self, model: ModelT, field_name: str, new_value: object) -> ModelT:
        """Updates the specified field of the specified model and returns the new model
        (or the same model if the update was in-place). Implementations are responsible
        for performing validation as the concrete model would."""

    def assert_property_valid_value(
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
        assert actual_value == initial_value, (
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"
        )

        # Act: update the model
        new_model = self.update_model(model, field_name, new_value)

        # Assert: the value is updated
        actual_value = getattr(new_model, field_name)
        assert actual_value == new_value, (
            f"After setting, value of {field_name} should be {new_value}, but got {actual_value}"
        )

    def assert_property_invalid_value(
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
        assert actual_value == initial_value, (
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"
        )

        # Assert: updating the model with an invalid value should fail
        with pytest.raises(ValueError):
            self.update_model(model, field_name, invalid_value)

    def assert_property_normalization(
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
        assert actual_value == initial_value, (
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"
        )

        # Act: set the value
        new_model = self.update_model(model, field_name, input_value)

        # Assert: the value is normalized as expected
        assert getattr(new_model, field_name) == expected_value
