from typing import TypeVar, Generic, Sequence, Iterable, MutableSequence, Optional, cast, overload, List, Iterator, \
    SupportsIndex
from PySide6.QtCore import QObject, Signal

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
