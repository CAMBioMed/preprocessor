from pathlib import Path
from typing import TypeVar, Any, Self

from PySide6.QtCore import QObject, Signal
from pydantic import BaseModel, ValidationError
import contextlib

M = TypeVar("M", bound=BaseModel)

class QModel[M: BaseModel](QObject):
    """
    Reusable base class that holds a Pydantic model instance and provides
    helpers for setting fields with validation and emitting change signals.

    Subclasses should either pass model_cls to __init__ or call super().__init__(model_cls=YourModel).
    Subclasses are expected to declare per-field signals named on_<field>_changed if desired;
    base will call them when that field changes.
    """

    on_changed: Signal = Signal()
    """Signal emitted whenever the model is modified."""
    on_dirty_changed: Signal = Signal(bool)
    """Signal emitted when the dirty state changes."""
    _model_cls: type[M]
    _model_version: int
    _data: M
    _dirty: bool

    def __init__(
        self,
        model_cls: type[M],
        data: M | dict[str, Any] | None,
    ) -> None:
        super().__init__()
        self._model_cls = model_cls
        self._model_version = int(getattr(model_cls, "SERIAL_VERSION", 1))
        self._set_data(data)

    def _set_data(self, data: M | dict[str, Any] | None) -> None:
        if data is None:
            # No initial data provided; create a default instance of the model
            self._data = self._model_cls()  # type: ignore[assignment]
        elif isinstance(data, BaseModel):
            # Assume it's already validated and of the correct type; assign directly
            self._data = data  # type: ignore[assignment]
        else:
            # Let pydantic validate and parse
            self._data = self._model_cls.model_validate(data)  # type: ignore[assignment]

        self._dirty = False

    def _populate_lists_from_data(self) -> None:
        """
        Populate any QListModel children from the current data.

        This is called after deserialization to ensure that the interactive list models reflect the current data.
        """
        # This method is meant to be overridden by subclasses that have QListModel children.
        pass

    @property
    def dirty(self) -> bool:
        """True if model has been modified since last clear_dirty()."""
        return self._dirty

    def _set_dirty(self, value: bool) -> None:
        """
        Update dirty state.

        Propagates clean state to the children, and emits on_dirty_changed when it changes.
        """
        if self._dirty == value:
            return
        self._dirty = value
        if not value:
            # Propagate clean state to children
            from preprocessor.model.qlistmodel import QListModel  # noqa: PLC0415

            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if isinstance(attr, (QModel, QListModel)):
                    attr.mark_clean()
        with contextlib.suppress(Exception):
            self.on_dirty_changed.emit(value)

    def mark_dirty(self) -> None:
        """Mark the model as dirty (set dirty flag to True)."""
        self._set_dirty(True)

    def mark_clean(self) -> None:
        """Clear the dirty flag (set to False) recursively."""
        self._set_dirty(False)

    def _emit_field_signal(self, field_name: str) -> None:
        sig = getattr(self, f"on_{field_name}_changed", None)
        if sig is not None and hasattr(sig, "emit"):
            with contextlib.suppress(Exception):
                sig.emit()

    def _set_field(self, field: str, value: Any) -> None:  # noqa: ANN401
        """
        Validate and set a single field using the pydantic model.

        Emits per-field and on_changed signals only if the validated model differs from the previous one.
        """
        if field not in self._model_cls.model_fields:
            raise ValueError(f"{field!r} is not a valid field in this model's data")

        # We mutate the existing model, such that all references to it get the updated data
        old_data = self._data.model_copy()
        setattr(self._data, field, value)
        new_data = self._data

        if new_data != old_data:
            self._set_dirty(True)
            if getattr(new_data, field) != getattr(old_data, field):
                self._emit_field_signal(field)
            with contextlib.suppress(Exception):
                self.on_changed.emit()

