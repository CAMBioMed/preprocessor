from typing import TypeVar, Generic, Sequence, Iterable, MutableSequence, Optional, cast, overload, List
from PySide6.QtCore import QObject, Signal

E = TypeVar("E", bound=QObject)


class QListModel(QObject, Generic[E]):
    """
    A list-like container for QObjects that automatically manages parent-child relationships.
    """

    on_changed: Signal = Signal()
    """Signal emitted whenever the list is modified."""

    def __init__(self, iterable: Optional[Iterable[E]] = None, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._items: List[E] = []
        if iterable:
            for item in iterable:
                self.append(item)

    def __len__(self) -> int:
        return len(self._items)

    @overload
    def __getitem__(self, index: int) -> E:
        pass

    @overload
    def __getitem__(self, index: slice) -> list[E]:
        pass

    def __getitem__(self, index: int | slice) -> E | list[E]:
        return self._items[index]

    @overload
    def __setitem__(self, index: int, value: E) -> None:
        pass

    @overload
    def __setitem__(self, index: slice, value: Iterable[E]) -> None:
        pass

    def __setitem__(self, index: int | slice, value: E | Iterable[E]) -> None:
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
        else:
            if not isinstance(value, QObject):
                raise TypeError("QObjectList only accepts QObjects")
            old = self._items[index]
            old.setParent(None)
            value.setParent(self)
            self._items[index] = value
        self.on_changed.emit()

    @overload
    def __delitem__(self, index: int) -> None:
        pass

    @overload
    def __delitem__(self, index: slice) -> None:
        pass

    def __delitem__(self, index: int | slice) -> None:
        items = self._items[index] if isinstance(index, slice) else [self._items[index]]
        for item in items:
            item.setParent(None)
        del self._items[index]
        self.on_changed.emit()

    def insert(self, index: int, value: E) -> None:
        if not isinstance(value, QObject):
            raise TypeError("QObjectList only accepts QObjects")
        value.setParent(self)
        self._items.insert(index, value)
        self.on_changed.emit()

    def append(self, value: E) -> None:
        self.insert(len(self._items), value)
