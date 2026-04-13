from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Generic

import pytest
from pydantic import BaseModel
from pytestqt.qtbot import QtBot

from preprocessor.model.qmodel import QModel

# Make this base test generic over the pydantic model type being tested.
QModelT = TypeVar("QModelT", bound=QModel)

class QModelTestBase(ABC, Generic[QModelT]):

    # def assert_model_property_signals_on_mutation(
    #     self,
    #     qtbot: QtBot,
    #     model: QModelT,
    #     prop_name: str,
    #     fn_set_same: Callable[[QModelT, str], None],
    #     fn_set_new: Callable[[QModelT, str], None],
    # ) -> None:
    #     """Helper to assert getter, setter, and per-field signal emission for QModel properties.
    #
    #     :param qtbot: pytest-qt's QtBot fixture for signal assertions
    #     :param model: the QModel instance to test
    #     :param prop_name: the name of the property to test (e.g., "date")
    #     :param fn_set_same: a function that sets the property to the same value (should not emit signals)
    #     :param fn_set_new: a function that sets the property to a different value (should emit signals)
    #     """
    #
    #     try:
    #         on_field_signal = getattr(model, f"on_{prop_name}_changed")
    #     except AttributeError:
    #         raise AssertionError(
    #             f"Model {type(model).__name__} does not have a signal named on_{prop_name}_changed") from None
    #     on_changed_signal = model.on_changed
    #
    #     # Assert: model is not dirty
    #     assert not model.dirty, "Model should not be dirty before mutation, but it is."
    #
    #     # Assert: setting the same value should not emit any signals
    #     # noinspection PyTypeChecker
    #     with qtbot.assertNotEmitted(on_changed_signal), qtbot.assertNotEmitted(on_field_signal):
    #         fn_set_same(model, prop_name)
    #
    #     # Assert: model is still not dirty
    #     assert not model.dirty, "Model should not be dirty after setting the same value, but it is."
    #
    #     # Assert: setting a different value should emit signals
    #     with qtbot.waitSignals([on_changed_signal, on_field_signal], timeout=1000):
    #         fn_set_new(model, prop_name)
    #
    #     # Assert: model is now dirty
    #     assert model.dirty, "Model should be dirty after setting a new value, but it is not."
    #
    #     # Act: clean the model
    #     model.mark_clean()
    #

    @abstractmethod
    def create_model(self) -> QModelT:
        """Return an empty/new instance of the model under test."""

    def assert_property_valid_value_and_signals(
        self,
        field_name: str,
        initial_value: object,
        new_value: object,
        qtbot: QtBot,
    ) -> None:
        """Model properties can be set to a valid value."""
        # Arrange: empty model
        model = self.create_model()

        # Assert: the initial value is as expected
        actual_value = getattr(model, field_name)
        assert actual_value == initial_value, \
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"

        # Act: update the model
        new_model = self.assert_model_property_signals_on_mutation(
            qtbot,
            model,
            field_name,
            fn_set_same=lambda m, p: setattr(m, p, initial_value),
            fn_set_new=lambda m, p: setattr(m, p, new_value),
        )

        # Assert: the value is updated
        actual_value = getattr(new_model, field_name)
        assert actual_value == new_value, \
            f"After setting, value of {field_name} should be {new_value}, but got {actual_value}"

    def assert_property_invalid_value_and_signals(
        self,
        field_name: str,
        initial_value: object,
        invalid_value: object,
        qtbot: QtBot,
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
            self.assert_model_property_signals_on_mutation(
                qtbot,
                model,
                field_name,
                fn_set_same=lambda m, p: setattr(m, p, initial_value),
                fn_set_new=lambda m, p: setattr(m, p, invalid_value),
            )

    def assert_property_normalization_and_signals(
        self,
        field_name: str,
        initial_value: object,
        input_value: object,
        expected_value: object,
        qtbot: QtBot,
    ) -> None:
        """Model properties should normalize (trimming, empty to None) on assignment."""
        # Arrange: empty model
        model = self.create_model()

        # Assert: the initial value is as expected
        actual_value = getattr(model, field_name)
        assert actual_value == initial_value, \
            f"Initial value of {field_name} should be {initial_value}, but got {actual_value}"

        # Act: set the value
        new_model = self.assert_model_property_signals_on_mutation(
            qtbot,
            model,
            field_name,
            fn_set_same=lambda m, p: setattr(m, p, initial_value),
            fn_set_new=lambda m, p: setattr(m, p, input_value),
        )

        # Assert: the value is normalized as expected
        assert getattr(new_model, field_name) == expected_value

    def assert_model_property_signals_on_mutation(
        self,
        qtbot: QtBot,
        model: QModelT,
        prop_name: str,
        fn_set_same: Callable[[QModelT, str], None],
        fn_set_new: Callable[[QModelT, str], None],
    ) -> QModelT:
        """Helper to assert getter, setter, and per-field signal emission for QModel properties.

        :param qtbot: pytest-qt's QtBot fixture for signal assertions
        :param model: the QModel instance to test
        :param prop_name: the name of the property to test (e.g., "date")
        :param fn_set_same: a function that sets the property to the same value (should not emit signals)
        :param fn_set_new: a function that sets the property to a different value (should emit signals)
        """

        try:
            on_field_signal = getattr(model, f"on_{prop_name}_changed")
        except AttributeError:
            raise AssertionError(
                f"Model {type(model).__name__} does not have a signal named on_{prop_name}_changed") from None
        on_changed_signal = model.on_changed

        # Assert: model is not dirty
        assert not model.dirty, "Model should not be dirty before mutation, but it is."

        # Assert: setting the same value should not emit any signals
        # noinspection PyTypeChecker
        with qtbot.assertNotEmitted(on_changed_signal), qtbot.assertNotEmitted(on_field_signal):
            fn_set_same(model, prop_name)

        # Assert: model is still not dirty
        assert not model.dirty, "Model should not be dirty after setting the same value, but it is."

        # Assert: setting a different value should emit signals
        with qtbot.waitSignals([on_changed_signal, on_field_signal], timeout=1000):
            fn_set_new(model, prop_name)

        # Assert: model is now dirty
        assert model.dirty, "Model should be dirty after setting a new value, but it is not."

        # Act: clean the model
        model.mark_clean()

        return model

    # def assert_model_property_getter_setter_and_signal(
    #     self,
    #     qtbot: QtBot,
    #     model: QModelT,
    #     prop_name: str,
    #     initial_value: object,
    #     new_value: object,
    # ) -> QModelT:
    #     """Helper to assert getter, setter, and per-field signal emission for QModel properties.
    #
    #     :param qtbot: pytest-qt's QtBot fixture for signal assertions
    #     :param model: the QModel instance to test
    #     :param prop_name: the name of the property to test (e.g., "date")
    #     :param initial_value: the expected initial value of the property
    #     :param new_value: a different value to set, which should trigger signals
    #     """
    #
    #     # Assert: initial value is as expected
    #     actual_value = getattr(model, prop_name)
    #     assert getattr(model, prop_name) == initial_value, \
    #         f"Expected initial value of {prop_name} to be {initial_value}, but got {actual_value}"
    #
    #     self.assert_model_property_signals_on_mutation(
    #         qtbot,
    #         model,
    #         prop_name,
    #         fn_set_same=lambda m, p: setattr(m, p, initial_value),
    #         fn_set_new=lambda m, p: setattr(m, p, new_value),
    #     )
    #
    #     # Assert: the value is updated
    #     assert getattr(model, prop_name) == new_value

    def assert_has_a_property_for_each_data_field(
        self,
        model_class: type[QModel],
        data_model_class: type[BaseModel],
    ) -> None:
        """Model should have a property for each field in the data model."""
        expected_fields = set(data_model_class.model_fields.keys())
        model_fields = set()
        for attr_name in dir(model_class):
            attr = getattr(model_class, attr_name)
            if isinstance(attr, property):
                model_fields.add(attr_name)
        missing_fields = expected_fields - model_fields
        assert not missing_fields, f"{model_class.__name__} is missing properties for fields: {missing_fields}"
