from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDockWidget, QWidget, QListWidget, QListWidgetItem


class ThumbnailListWidget(QDockWidget):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Thumbnails", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea)

        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.thumbnail_list.setIconSize(QSize(100, 100))
        self.thumbnail_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.thumbnail_list.setSpacing(10)

        self.setWidget(self.thumbnail_list)

    def add_thumbnail(self, image_path: str, label: str) -> None:
        item = QListWidgetItem(QIcon(image_path), label)
        self.thumbnail_list.addItem(item)

    def clear_thumbnails(self) -> None:
        self.thumbnail_list.clear()