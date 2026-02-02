from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QKeySequence
from PySide6.QtWidgets import QDockWidget, QWidget

from preprocessor.gui.ui_thumbnail_dock import Ui_ThumbnailDock


class ThumbnailDockWidget(QDockWidget):
    ui: Ui_ThumbnailDock

    def __init__(self, parent: QWidget | None = None) -> None:
        QDockWidget.__init__(self, parent)
        self.ui = Ui_ThumbnailDock()
        self.ui.setupUi(self)
        self._setup_icons()
        self._setup_keyboard_shortcuts()

    def _setup_icons(self) -> None:
        """Set up icons for actions."""
        # Toolbar
        self.ui.addPhotoAction.setIcon(QIcon(QIcon("src/preprocessor/icons/fugue16/image--plus.png")))
        self.ui.removeThumbnailAction.setIcon(QIcon(QIcon("src/preprocessor/icons/fugue16/image--minus.png")))


    def _setup_keyboard_shortcuts(self) -> None:
        """Set up keyboard shortcuts for actions."""
        # Toolbar
        self.ui.addPhotoAction.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_Equal)
        self.ui.removeThumbnailAction.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_Backspace)