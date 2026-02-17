from typing import TypeVar, Generic, Sequence, Iterable, MutableSequence, Optional, cast, overload, List, Iterator, \
    SupportsIndex, Type, Callable
from PySide6.QtCore import QObject, Signal
from pydantic import BaseModel

from preprocessor.model.qmodel import QModel

E = TypeVar("E", bound=QObject)


class QListModel(QObject, Generic[E]):
    """
    A list-like container for QObjects that automatically manages parent-child relationships.
    """

    # emit (added_items: list[E], removed_items: list[E])
    on_changed: Signal = Signal(list, list)
    """Signal emitted whenever the list is modified."""

    _items: List[E]

    def __init__(self, iterable: Optional[Iterable[E]] = None, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._items = []
        if iterable:
            for item in iterable:
                self.append(item)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[E]:
        """
        Allow iteration over the items in the QListModel.
        """
        return iter(self._items)

    @overload
    def __getitem__(self, index: SupportsIndex) -> E:
        pass

    @overload
    def __getitem__(self, index: slice) -> list[E]:
        pass

    def __getitem__(self, index: SupportsIndex | slice) -> E | list[E]:
        return self._items[index]

    @overload
    def __setitem__(self, index: SupportsIndex, value: E) -> None:
        pass

    @overload
    def __setitem__(self, index: slice, value: Iterable[E]) -> None:
        pass

    def __setitem__(self, index: SupportsIndex | slice, value: E | Iterable[E]) -> None:
        if isinstance(index, slice):
            items = list(value)  # type: ignore[arg-type,call-overload]
            for item in items:
                if not isinstance(item, QObject):
                    raise TypeError("QObjectList only accepts QObjects")
                item.setParent(self)
            old_items = self._items[index]
            for old in old_items:
                old.setParent(None)
            self._items[index] = items
            # emit added / removed lists
            self.on_changed.emit(items, list(old_items))
        else:
            if not isinstance(value, QObject):
                raise TypeError("QObjectList only accepts QObjects")
            old = self._items[index]
            old.setParent(None)
            value.setParent(self)
            self._items[index] = value
            self.on_changed.emit([value], [old])

    @overload
    def __delitem__(self, index: SupportsIndex) -> None:
        pass

    @overload
    def __delitem__(self, index: slice) -> None:
        pass

    def __delitem__(self, index: SupportsIndex | slice) -> None:
        items = self._items[index] if isinstance(index, slice) else [self._items[index]]
        for item in items:
            item.setParent(None)
        del self._items[index]
        # emit removed list
        self.on_changed.emit([], list(items))

    def insert(self, index: SupportsIndex, value: E) -> None:
        if not isinstance(value, QObject):
            raise TypeError("QObjectList only accepts QObjects")
        value.setParent(self)
        self._items.insert(index, value)
        # emit added list
        self.on_changed.emit([value], [])

    def append(self, value: E) -> None:
        self.insert(len(self._items), value)

    def remove(self, value: E) -> None:
        index = self._items.index(value)
        del self[index]

    def index(self, value: E) -> int:
        return self._items.index(value)

    def populate_from_data(self,
                           data_list: Iterable[BaseModel | dict] | None,
                           model_cls: Type[QModel]) -> None:
        """
        Replace the contents of this QListModel with `model_cls(data=...)` instances
        created from each element in `data_list` (which may be pydantic models or dicts).
        Uses slice assignment to produce a single on_changed emission.
        """
        if not data_list:
            # empty or None -> clear list
            self[:] = []
            return

        items: List[E] = []
        for d in data_list:
            # model_cls is expected to be a QModel subclass (returns a QObject)
            obj = model_cls(model_cls, data=d)  # type: ignore[arg-type]
            # type: ignore for runtime: obj is a QObject/QModel instance and is E-compatible
            items.append(cast(E, obj))
        self[:] = items

    def to_serializable_list(self) -> list[dict]:
        """
        Return a JSON-friendly list for serialization. Each child is expected
        to implement `serialize()` (QModel does); fall back to `_data.model_dump()`.
        """
        out: list[dict] = []
        for it in self._items:
            if hasattr(it, "serialize"):
                out.append(it.serialize())  # type: ignore[arg-type]
            else:
                # fallback to raw pydantic dump
                try:
                    out.append(it._data.model_dump())  # type: ignore[attr-defined]
                except Exception:
                    out.append({})
        return out

    def bind_to_model(self,
                      owner: QModel,
                      field_name: str,
                      child_changed_callback: Callable[..., None] | None = None) -> None:
        """
        Bind this QListModel to a parent `owner` (a QModel instance) and a pydantic
        `field_name`. Whenever the list changes this will:
          - connect `child.on_changed` -> `child_changed_callback` for added children
          - disconnect for removed children
          - call `owner._set_field(field_name, payload)` where payload is a list of
            plain dicts (or None if empty)

        Note: `owner._set_field` is used to validate and update the owner's pydantic model.
        """
        def _handler(added: list[E], removed: list[E]) -> None:
            # wire/unwire child change handlers
            if child_changed_callback is not None:
                for a in added:
                    try:
                        a.on_changed.connect(child_changed_callback)  # type: ignore[attr-defined]
                    except Exception:
                        pass
                for r in removed:
                    try:
                        r.on_changed.disconnect(child_changed_callback)  # type: ignore[attr-defined]
                    except Exception:
                        pass

            payload = [getattr(item, "_data").model_dump() for item in self._items] if len(self._items) > 0 else []
            # validate & update owner model (marks owner dirty if changed)
            owner._set_field(field_name, payload)

        # connect handler
        self.on_changed.connect(_handler)