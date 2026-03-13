from pydantic import BaseModel
from pytestqt.qtbot import QtBot

from preprocessor.model.qmodel import QModel


def assert_model_property_getter_setter_and_signal(
    qtbot: QtBot,
    model: QModel,
    prop_name: str,
    initial_value: object,
    new_value: object,
) -> None:
    """Helper to assert getter, setter, and per-field signal emission for QModel properties.

    :param qtbot: pytest-qt's QtBot fixture for signal assertions
    :param model: the QModel instance to test
    :param prop_name: the name of the property to test (e.g., "date")
    :param initial_value: the expected initial value of the property
    :param new_value: a different value to set, which should trigger signals
    """

    on_field_signal = getattr(model, f"on_{prop_name}_changed")
    on_changed_signal = model.on_changed

    # Assert: initial value is as expected
    assert getattr(model, prop_name) == initial_value

    # Assert: model is not dirty
    assert not model.dirty

    # Assert: setting the same value should not emit any signals
    # noinspection PyTypeChecker
    with qtbot.assertNotEmitted(on_changed_signal), qtbot.assertNotEmitted(on_field_signal):
        setattr(model, prop_name, initial_value)

    # Assert: model is still not dirty
    assert not model.dirty

    # Assert: setting a different value should emit signals
    with qtbot.waitSignal(on_changed_signal, timeout=1000), qtbot.waitSignal(on_field_signal, timeout=1000):
        setattr(model, prop_name, new_value)

    # Assert: model is now dirty
    assert model.dirty

    # Assert: the value is updated
    assert getattr(model, prop_name) == new_value

    # Act: clean the model
    model.mark_clean()


def assert_has_a_property_for_each_data_field(
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