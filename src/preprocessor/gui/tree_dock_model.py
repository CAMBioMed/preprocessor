from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    Qt,
    Signal,
)
from PySide6.QtGui import QIcon

from preprocessor.gui.model import QPhotoModel
from preprocessor.gui.utils import icon_from_resource

_INVALID_INDEX = QModelIndex()
_FOLDER_CLOSED_ICON_RESOURCE = "icons/fugue16/folder.png"
_FOLDER_OPEN_ICON_RESOURCE = "icons/fugue16/folder-open.png"


@dataclass
class _DirectoryNode:
    path: Path
    parent: "_DirectoryNode | None"
    children: list["_DirectoryNode"] = field(default_factory=list)


class TreeDockModel(QAbstractItemModel):
    """Expose project photo directories as a one-column Qt tree model."""

    on_active_directory_changed = Signal(object)

    def __init__(self, parent: QObject | None = None) -> None:
        """Create an empty directory tree model."""
        super().__init__(parent)
        self._roots: list[_DirectoryNode] = []
        self._nodes_by_path: dict[Path, _DirectoryNode] = {}
        self._photos_by_directory: dict[Path, list[QPhotoModel]] = {}
        self._active_directory: Path | None = None
        self._folder_closed_icon: QIcon | None = None
        self._folder_open_icon: QIcon | None = None

    def index(
        self,
        row: int,
        column: int,
        parent: QModelIndex | QPersistentModelIndex = _INVALID_INDEX,
    ) -> QModelIndex:
        """Return the index at *row* and *column* below *parent*."""
        if row < 0 or column != 0:
            return QModelIndex()
        if parent.isValid():
            parent_node = self._node_for_index(parent)
            if parent_node is None or parent.column() != 0:
                return QModelIndex()
            children = parent_node.children
        else:
            children = self._roots
        if row >= len(children):
            return QModelIndex()
        return self.createIndex(row, column, children[row])

    # There are two parent() methods to override, we override the one in QAbstractItemModel.
    # This is correct, but because this confuses all the type checking tools, we ignore these errors.
    def parent(  # type: ignore[override]  # ty: ignore[invalid-method-override]
        self, index: QModelIndex | QPersistentModelIndex
    ) -> QModelIndex:
        """Return the parent index for *index*."""
        node = self._node_for_index(index)
        if node is None or node.parent is None:
            return QModelIndex()
        parent_node = node.parent
        siblings = parent_node.parent.children if parent_node.parent is not None else self._roots
        return self.createIndex(siblings.index(parent_node), 0, parent_node)

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = _INVALID_INDEX) -> int:
        """Return the number of directory children below *parent*."""
        if parent.isValid():
            node = self._node_for_index(parent)
            if node is None or parent.column() != 0:
                return 0
            return len(node.children)
        return len(self._roots)

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = _INVALID_INDEX) -> int:
        """Return the single directory-name column count."""
        if parent.isValid() and self._node_for_index(parent) is None:
            return 0
        return 1

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> object | None:
        """Return display or tooltip data for a directory index."""
        node = self._node_for_index(index)
        if node is None or index.column() != 0:
            return None
        if role == Qt.ItemDataRole.DecorationRole:
            if self._folder_closed_icon is None:
                self._folder_closed_icon = icon_from_resource(_FOLDER_CLOSED_ICON_RESOURCE)
            if self._folder_open_icon is None:
                self._folder_open_icon = icon_from_resource(_FOLDER_OPEN_ICON_RESOURCE)
            return self._folder_open_icon if node.path == self._active_directory else self._folder_closed_icon
        if role == Qt.ItemDataRole.DisplayRole:
            return node.path.name or str(node.path)
        if role == Qt.ItemDataRole.ToolTipRole:
            return str(node.path)
        return None

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        """Return selectable, enabled flags for valid directory indexes."""
        if self._node_for_index(index) is None or index.column() != 0:
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def set_photos(
        self,
        photos: Iterable[QPhotoModel],
        *,
        project_directory: Path | None,
        reset_active: bool = False,
    ) -> None:
        """Rebuild the directory tree from *photos* beneath *project_directory*.

        Raises:
            ValueError: If photos are supplied without a project directory or a photo is outside it.
        """
        photo_list = list(photos)
        if photo_list and project_directory is None:
            message = "project directory is required when photos are present"
            raise ValueError(message)

        root_path = project_directory.resolve() if project_directory is not None else None
        grouped: dict[Path, list[QPhotoModel]] = {}
        relative_directories: list[tuple[Path, Path]] = []
        if root_path is not None:
            for photo in photo_list:
                photo_directory = photo.original_filename.parent
                try:
                    relative_directory = photo_directory.relative_to(root_path)
                except ValueError as error:
                    message = f"photo path is outside project directory: {photo.original_filename}"
                    raise ValueError(message) from error
                grouped.setdefault(photo_directory, []).append(photo)
                relative_directories.append((photo_directory, relative_directory))

        old_active = self._active_directory
        self.beginResetModel()
        self._roots = []
        self._nodes_by_path = {}
        self._photos_by_directory = grouped

        if photo_list and root_path is not None:
            root = _DirectoryNode(root_path, None)
            self._roots.append(root)
            self._nodes_by_path[root_path] = root
            for _, relative_directory in relative_directories:
                parent_node = root
                current_path = root_path
                for segment in relative_directory.parts:
                    current_path /= segment
                    node = self._nodes_by_path.get(current_path)
                    if node is None:
                        node = _DirectoryNode(current_path, parent_node)
                        parent_node.children.append(node)
                        self._nodes_by_path[current_path] = node
                    parent_node = node
            for node in self._nodes_by_path.values():
                node.children.sort(key=lambda child: (str(child.path).casefold(), str(child.path)))

        if not photo_list:
            final_active = None
        elif not reset_active and old_active in self._nodes_by_path:
            final_active = old_active
        else:
            final_active = min(grouped, key=lambda path: (str(path).casefold(), str(path)))
        self._active_directory = final_active
        self.endResetModel()

        if final_active != old_active:
            self.on_active_directory_changed.emit(final_active)

    @property
    def active_directory(self) -> Path | None:
        """Return the directory whose direct photos should be displayed, or ``None``."""
        return self._active_directory

    @active_directory.setter
    def active_directory(self, directory: Path | None) -> None:
        """Select an exact directory present in the tree, or clear the selection.

        Raises:
            ValueError: If *directory* is not present in the current tree.
        """
        if directory is not None and directory not in self._nodes_by_path:
            message = f"directory is not present in tree: {directory}"
            raise ValueError(message)
        if directory == self._active_directory:
            return
        old_directory = self._active_directory
        self._active_directory = directory
        for changed_directory in (old_directory, directory):
            if changed_directory is not None:
                changed_index = self.index_for_directory(changed_directory)
                if changed_index.isValid():
                    self.dataChanged.emit(changed_index, changed_index, [Qt.ItemDataRole.DecorationRole])
        self.on_active_directory_changed.emit(directory)

    def directory_for_index(self, index: QModelIndex) -> Path | None:
        """Return the directory represented by an index owned by this model."""
        node = self._node_for_index(index)
        return node.path if node is not None and index.column() == 0 else None

    def index_for_directory(self, directory: Path) -> QModelIndex:
        """Return the model index for an exact directory path, if present."""
        node = self._nodes_by_path.get(directory)
        if node is None:
            return QModelIndex()
        siblings = node.parent.children if node.parent is not None else self._roots
        return self.createIndex(siblings.index(node), 0, node)

    def photos_in_directory(self, directory: Path | None) -> list[QPhotoModel]:
        """Return a new list of photos whose immediate parent is *directory*."""
        if directory is None:
            return []
        return list(self._photos_by_directory.get(directory, ()))

    def _node_for_index(self, index: QModelIndex | QPersistentModelIndex) -> _DirectoryNode | None:
        if not index.isValid() or index.model() is not self:
            return None
        node = index.internalPointer()
        if not isinstance(node, _DirectoryNode):
            return None
        if self._nodes_by_path.get(node.path) is not node:
            return None
        return node
