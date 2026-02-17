from pathlib import Path
from typing import Generic, Type, TypeVar, Any

from PySide6.QtCore import QObject, Signal
from pydantic import BaseModel, ValidationError

M = TypeVar("M", bound=BaseModel)

def _to_basic(obj: Any) -> Any:
    """
    Convert nested tuples/lists/Paths/primitives to JSON-friendly basic Python types (lists, numbers, strings).
    """
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, (list, tuple)):
        return [_to_basic(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _to_basic(v) for k, v in obj.items()}
    return str(obj)  # Fallback


class QModel(QObject, Generic[M]):
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
    _model_cls: Type[M]
    _model_version: int
    _data: M
    _dirty: bool

    def __init__(self,
                 model_cls: Type[M],
                 data: M | dict[str, Any] | None = None,
     ) -> None:
        super().__init__()
        self._model_cls = model_cls
        self._model_version = int(getattr(model_cls, "SERIAL_VERSION", 1))
        if data is None:
            # No initial data provided; create a default instance of the model
            self._data = model_cls()  # type: ignore[assignment]
        elif isinstance(data, BaseModel):
            # Assume it's already validated and of the correct type; assign directly
            self._data = data  # type: ignore[assignment]
        else:
            # Let pydantic validate and parse
            self._data = model_cls.model_validate(data)  # type: ignore[assignment]

        self._dirty = False

    @property
    def dirty(self) -> bool:
        """True if model has been modified since last clear_dirty()."""
        return self._dirty

    def _set_dirty(self, value: bool) -> None:
        """Internal helper to update dirty state and emit dirty_changed when it changes."""
        if self._dirty != value:
            self._dirty = value
            try:
                self.on_dirty_changed.emit(value)
            except Exception:
                pass

    def mark_dirty(self) -> None:
        """Mark the model as dirty (set dirty flag to True)."""
        self._set_dirty(True)

    def mark_clean(self) -> None:
        """Clear the dirty flag (set to False) recursively."""
        from preprocessor.model.qlistmodel import QListModel

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QModel):
                attr.mark_clean()
            elif isinstance(attr, QListModel):
                attr.mark_clean()
        self._set_dirty(False)

    def _emit_field_signal(self, field_name: str) -> None:
        sig = getattr(self, f"on_{field_name}_changed", None)
        if sig is not None and hasattr(sig, "emit"):
            try:
                sig.emit()
            except Exception:
                # Ignore emit failures to avoid breaking model flow
                pass


    def _set_field(self, field: str, value: Any) -> None:
        """
        Validate and set a single field using the pydantic model.

        Emits per-field and on_changed signals only if the validated model differs from the previous one.
        """
        old = self._data.model_dump()

        merged = {**old, field: value}
        try:
            new_model = self._model_cls.model_validate(merged)  # type: ignore[arg-type]
        except ValidationError as exc:
            raise ValueError(str(exc)) from exc

        new = new_model.model_dump()
        if new != old:
            self._data = new_model
            if new.get(field) != old.get(field):
                self._emit_field_signal(field)
            self._set_dirty(True)
            try:
                self.on_changed.emit()
            except Exception:
                pass


    def serialize(self) -> dict[str, Any]:
        """Return a JSON-friendly dict (Paths -> str, tuples -> lists)."""
        d = self._data.model_dump()
        out = {k: _to_basic(v) for k, v in d.items()}
        out["model_version"] = int(self._model_version)
        return out


    def deserialize(self, data: dict[str, Any]) -> None:
        """
        Merge `data` into the current model and validate; only keys present in `data` are considered
        for emitting per-field signals. Emits on_changed if anything changed.
        """
        old = self._data.model_dump()
        incoming = dict(data)  # shallow copy

        # Ensure the model version matches
        if "model_version" not in incoming:
            raise ValueError(f"Missing 'model_version' field in serialized data; expected version {self._model_version}")
        try:
            incoming_model_version = int(incoming["model_version"])
        except Exception:
            raise ValueError(f"Invalid 'model_version' value: {incoming.get('model_version')!r}")
        if incoming_model_version != self._model_version:
            raise ValueError(f"Version mismatch: expected {self._model_version}, got {incoming_model_version}")
        incoming.pop("model_version", None)

        # Update the model
        merged = {**old}
        merged.update(incoming)
        try:
            new_model = self._model_cls.model_validate(merged)  # type: ignore[arg-type]
        except ValidationError as exc:
            raise ValueError(str(exc)) from exc

        # Update the data and emit signals for any fields that changed
        new = new_model.model_dump()
        if new != old:
            self._data = new_model
            for key in incoming.keys():
                if new.get(key) != old.get(key):
                    self._emit_field_signal(key)
            self._set_dirty(True)
            try:
                self.on_changed.emit()
            except Exception:
                pass
