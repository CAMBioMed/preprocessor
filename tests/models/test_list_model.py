from typing import Any

from PySide6.QtCore import QCoreApplication
import pytest
from PySide6.QtWidgets import QApplication

from pydantic import BaseModel

from preprocessor.model.qlistmodel import QListModel

from preprocessor.model.qmodel import QModel

# Ensure a Qt application context exists for QObject usage in tests. Rely on pytest-qt's qapp.
@pytest.fixture(autouse=True)
def _ensure_qapp(qapp: QApplication) -> QApplication:
    return qapp


class ItemData(BaseModel):
    name: str


class Item(QModel[ItemData]):
    def __init__(self, data: ItemData | dict[str, Any] | None = None) -> None:
        super().__init__(model_cls=ItemData, data=data)

    @property
    def name(self) -> str:
        return self._data.name

    @name.setter
    def name(self, value: str) -> None:
        self._set_field("name", value)

    def __repr__(self) -> str:
        return f"Item({self.name})"


@pytest.fixture()
def model() -> QListModel[Item]:
    return QListModel[Item]()

class TestQListModel:

    def test_append_and_len_and_parent(self, model: QListModel[Item]) -> None:
        # Arrange
        it = Item(ItemData(name="a"))

        # Act
        model.append(it)

        # Assert
        assert len(model) == 1
        assert it.parent() is model

    def test_insert(self, model: QListModel[Item]) -> None:
        # Arrange
        a = Item(ItemData(name="a"))
        b = Item(ItemData(name="b"))
        model.append(a)

        # Act
        model.insert(0, b)

        # Assert
        assert model[0] == b
        assert model[1] == a
        assert b.parent() is model

    def test_getitem_index_and_slice(self, model: QListModel[Item]) -> None:
        # Arrange
        items = [Item(ItemData(name=str(i))) for i in range(5)]
        for it in items:
            model.append(it)

        # Act
        single = model[2]
        sl = model[1:4]

        # Assert
        assert single is items[2]
        assert sl == items[1:4]
        assert sl[0].parent() is model

    def test_setitem_index(self, model: QListModel[Item]) -> None:
        # Arrange
        a = Item(ItemData(name="a"))
        b = Item(ItemData(name="b"))
        model.append(a)

        # Act
        model[0] = b

        # Assert
        assert a.parent() is None
        assert b.parent() is model
        assert model[0] == b

    def test_setitem_slice(self, model: QListModel[Item]) -> None:
        # Arrange
        orig = [
            Item(ItemData(name="1")),
            Item(ItemData(name="2")),
            Item(ItemData(name="3")),
            Item(ItemData(name="4")),
        ]
        for it in orig:
            model.append(it)
        replacements = [
            Item(ItemData(name="x")),
            Item(ItemData(name="y")),
        ]

        # Act
        model[1:3] = replacements

        # Assert
        assert orig[1].parent() is None
        assert orig[2].parent() is None
        assert model[1] is replacements[0]
        assert model[2] is replacements[1]
        assert replacements[0].parent() is model
        assert replacements[1].parent() is model

    def test_delitem_index_and_slice(self, model: QListModel[Item]) -> None:
        # Arrange
        items = [Item(ItemData(name=str(i))) for i in range(4)]
        for it in items:
            model.append(it)

        # Act: delete single index
        del model[1]

        # Assert after single delete
        assert len(model) == 3
        assert items[1].parent() is None

        # Act: delete a slice
        del model[0:2]

        # Assert after slice delete
        assert len(model) == 1
        assert items[0].parent() is None
        assert items[2].parent() is None
        assert model[0].parent() is model

    def test_type_errors(self, model: QListModel[Item]) -> None:
        # Arrange/Act/Assert for append non-QObject
        with pytest.raises(TypeError):
            # Act
            model.append(object())  # type: ignore[arg-type]

        # Insert non-QObject
        with pytest.raises(TypeError):
            model.insert(0, object())  # type: ignore[arg-type]
        # setitem index to non-QObject (need an existing item first)
        model.append(Item(ItemData(name="a")))
        with pytest.raises(TypeError):
            model[0] = object()  # type: ignore[call-overload]
        # setitem slice with non-QObject in iterable
        with pytest.raises(TypeError):
            model[0:1] = [object()]  # type: ignore[list-item]

    def test_on_changed_signal_emitted(self, model: QListModel[Item]) -> None:
        # Arrange
        calls = []

        def slot(added: list[Item], removed: list[Item]) -> None:
            calls.append((list(added), list(removed)))

        model.on_changed.connect(slot)

        # Act/Assert
        model.append(Item(ItemData(name="a")))
        assert len(calls) == 1
        model.insert(0, Item(ItemData(name="b")))
        assert len(calls) == 2
        model[0] = Item(ItemData(name="c"))
        assert len(calls) == 3
        del model[0]
        assert len(calls) == 4
        model[0:0] = [Item(ItemData(name="d"))]
        assert len(calls) == 5

    def test_iterable(self, model: QListModel[Item]) -> None:
        # Arrange
        items = [Item(ItemData(name=str(i))) for i in range(3)]
        for it in items:
            model.append(it)

        # Act: collect via list()
        collected = list(model)

        # Assert list() produced the same order and items, and parents are intact
        assert collected == items
        for it in collected:
            assert it.parent() is model

        # Act: use for-in loop to gather names
        names = []
        for it in model:
            names.append(it.name)

        # Assert
        assert names == ["0", "1", "2"]

        # Act: iter() returns an iterator
        it_obj = iter(model)
        assert hasattr(it_obj, "__next__")
