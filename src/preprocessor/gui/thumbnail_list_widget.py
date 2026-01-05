from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDockWidget, QWidget, QListWidget, QListWidgetItem

from preprocessor.gui.thumbnail_list_model import ThumbnailListModel


class ThumbnailListWidget(QDockWidget):

    model: ThumbnailListModel

    on_thumbnail_selected: Signal = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Thumbnails", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea)

        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.thumbnail_list.setIconSize(QSize(100, 100))
        self.thumbnail_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.thumbnail_list.setSpacing(10)

        self.setWidget(self.thumbnail_list)

        self.model = ThumbnailListModel()
        self._connect_signals()

    def _connect_signals(self) -> None:

        def _update_thumbnails() -> None:
            self.thumbnail_list.clear()
            for image_path in self.model.image_paths:
                label = image_path.split("/")[-1]  # Use filename as label
                item = QListWidgetItem(QIcon(image_path), label)
                self.thumbnail_list.addItem(item)

        self.model.on_image_paths_changed.connect(_update_thumbnails)

        def _on_item_clicked(item: QListWidgetItem) -> None:
            index = self.thumbnail_list.row(item)
            image_path = self.model.image_paths[index]
            self.on_thumbnail_selected.emit(image_path)

        self.thumbnail_list.itemClicked.connect(_on_item_clicked)
