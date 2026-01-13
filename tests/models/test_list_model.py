import unittest

from PySide6.QtCore import QObject, QCoreApplication
from preprocessor.model.list_model import QListModel

# Ensure a Qt application context exists for QObject usage in tests
if QCoreApplication.instance() is None:
    QCoreApplication([])


class Item(QObject):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __repr__(self) -> str:
        return f"Item({self.name})"
        
class TestQListModel(unittest.TestCase):

    def setUp(self) -> None:
        # Arrange: create an empty model (do not use subscription at runtime)
        self.model = QListModel[Item]()

    def test_append_and_len_and_parent(self) -> None:
        # Arrange
        it = Item("a")

        # Act
        self.model.append(it)

        # Assert
        self.assertEqual(len(self.model), 1)
        self.assertIs(it.parent(), self.model)

    def test_insert(self) -> None:
        # Arrange
        a = Item("a")
        b = Item("b")
        self.model.append(a)

        # Act
        self.model.insert(0, b)

        # Assert
        self.assertEqual(self.model[0], b)
        self.assertEqual(self.model[1], a)
        self.assertIs(b.parent(), self.model)

    def test_getitem_index_and_slice(self) -> None:
        # Arrange
        items = [Item(str(i)) for i in range(5)]
        for it in items:
            self.model.append(it)

        # Act
        single = self.model[2]
        sl = self.model[1:4]

        # Assert
        self.assertIs(single, items[2])
        self.assertEqual(sl, items[1:4])
        self.assertIs(sl[0].parent(), self.model)

    def test_setitem_index(self) -> None:
        # Arrange
        a = Item("a")
        b = Item("b")
        self.model.append(a)

        # Act
        self.model[0] = b

        # Assert
        self.assertIs(a.parent(), None)
        self.assertIs(b.parent(), self.model)
        self.assertEqual(self.model[0], b)

    def test_setitem_slice(self) -> None:
        # Arrange
        orig = [Item("1"), Item("2"), Item("3"), Item("4")]
        for it in orig:
            self.model.append(it)
        replacements = [Item("x"), Item("y")]

        # Act
        self.model[1:3] = replacements

        # Assert
        self.assertIs(orig[1].parent(), None)
        self.assertIs(orig[2].parent(), None)
        self.assertIs(self.model[1], replacements[0])
        self.assertIs(self.model[2], replacements[1])
        self.assertIs(replacements[0].parent(), self.model)
        self.assertIs(replacements[1].parent(), self.model)

    def test_delitem_index_and_slice(self) -> None:
        # Arrange
        items = [Item(str(i)) for i in range(4)]
        for it in items:
            self.model.append(it)

        # Act: delete single index
        del self.model[1]

        # Assert after single delete
        self.assertEqual(len(self.model), 3)
        self.assertIs(items[1].parent(), None)

        # Act: delete a slice
        del self.model[0:2]

        # Assert after slice delete
        self.assertEqual(len(self.model), 1)
        self.assertIs(items[0].parent(), None)
        self.assertIs(items[2].parent(), None)
        self.assertIs(self.model[0].parent(), self.model)

    def test_type_errors(self) -> None:
        # Arrange/Act/Assert for append non-QObject
        with self.assertRaises(TypeError):
            # Act
            self.model.append(object())  # type: ignore[arg-type]

        # Insert non-QObject
        with self.assertRaises(TypeError):
            self.model.insert(0, object())  # type: ignore[arg-type]
        # setitem index to non-QObject (need an existing item first)
        self.model.append(Item("a"))
        with self.assertRaises(TypeError):
            self.model[0] = object()   # type: ignore[call-overload]
        # setitem slice with non-QObject in iterable
        with self.assertRaises(TypeError):
            self.model[0:1] = [object()]   # type: ignore[list-item]

    def test_on_changed_signal_emitted(self) -> None:
        # Arrange
        calls = []

        def slot() -> None:
            calls.append(1)

        self.model.on_changed.connect(slot)

        # Act/Assert
        self.model.append(Item("a"))
        self.assertEqual(len(calls), 1)
        self.model.insert(0, Item("b"))
        self.assertEqual(len(calls), 2)
        self.model[0] = Item("c")
        self.assertEqual(len(calls), 3)
        del self.model[0]
        self.assertEqual(len(calls), 4)
        self.model[0:0] = [Item("d")]
        self.assertEqual(len(calls), 5)

