from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDockWidget, QWidget

from preprocessor.gui.ui_thumbnail_dock import Ui_ThumbnailDock


class ThumbnailDockWidget(QDockWidget):
    ui: Ui_ThumbnailDock

    def __init__(self, parent: QWidget | None = None) -> None:
        QDockWidget.__init__(self, parent)
        self.ui = Ui_ThumbnailDock()
        self.ui.setupUi(self)

    def _setup_icons(self) -> None:
        """Set up icons for actions."""
        self.ui.addPhotoAction.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.InsertImage)))