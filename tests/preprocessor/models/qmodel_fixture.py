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

    # Assert: setting the same value should not emit any signals
    # noinspection PyTypeChecker
    with qtbot.assertNotEmitted(on_changed_signal), qtbot.assertNotEmitted(on_field_signal):
        setattr(model, prop_name, initial_value)

    # Assert: setting a different value should emit signals
    with qtbot.waitSignal(on_changed_signal, timeout=1000), qtbot.waitSignal(on_field_signal, timeout=1000):
        setattr(model, prop_name, new_value)

    # Assert: the value is updated
    assert getattr(model, prop_name) == new_value
