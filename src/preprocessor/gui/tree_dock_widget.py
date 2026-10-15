from collections.abc import Iterable
from pathlib import Path

from PySide6.QtCore import QItemSelectionModel, QModelIndex
from PySide6.QtWidgets import QDockWidget, QWidget

from preprocessor.gui.designer.ui_tree_dock import Ui_TreeDock
from preprocessor.gui.model import QPhotoModel
from preprocessor.gui.tree_dock_model import TreeDockModel


class TreeDockWidget(QDockWidget):
    """Display and activate directories represented by project photos."""

    ui: Ui_TreeDock
    model: TreeDockModel

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create the dock and connect double-click directory activation."""
        super().__init__(parent)
        self.ui = Ui_TreeDock()
        self.ui.setupUi(self)
        self.model = TreeDockModel(self)
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.doubleClicked.connect(self._activate_index)
        self.model.modelReset.connect(self._synchronize_selection)
        self.model.on_active_directory_changed.connect(self._synchronize_selection)

    def set_photos(
        self,
        photos: Iterable[QPhotoModel],
        *,
        project_directory: Path | None,
        reset_active: bool = False,
    ) -> None:
        """Rebuild the displayed directories from the supplied project photos."""
        self.model.set_photos(
            photos,
            project_directory=project_directory,
            reset_active=reset_active,
        )

    def _activate_index(self, index: QModelIndex) -> None:
        directory = self.model.directory_for_index(index)
        if directory is not None:
            self.model.active_directory = directory

    def _synchronize_selection(self, *_args: object) -> None:
        tree_view = self.ui.treeView
        tree_view.collapseAll()
        active_directory = self.model.active_directory
        selection_model = tree_view.selectionModel()
        if active_directory is None:
            selection_model.clear()
            return

        active_index = self.model.index_for_directory(active_directory)
        if not active_index.isValid():
            selection_model.clear()
            return

        ancestors: list[QModelIndex] = []
        ancestor = active_index.parent()
        while ancestor.isValid():
            ancestors.append(ancestor)
            ancestor = ancestor.parent()
        for ancestor in reversed(ancestors):
            tree_view.expand(ancestor)

        flags = QItemSelectionModel.SelectionFlag.ClearAndSelect | QItemSelectionModel.SelectionFlag.Rows
        selection_model.setCurrentIndex(active_index, flags)
        selection_model.select(active_index, flags)
        tree_view.scrollTo(active_index)
