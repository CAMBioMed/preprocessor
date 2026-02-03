from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QKeySequence, QPixmap
from PySide6.QtWidgets import QDockWidget, QWidget, QListWidget, QListWidgetItem

from preprocessor.gui.ui_thumbnail_dock import Ui_ThumbnailDock
from preprocessor.model.list_model import QListModel
from preprocessor.model.photo_model import PhotoModel


class ThumbnailDockWidget(QDockWidget):
    ui: Ui_ThumbnailDock

    def __init__(self, parent: QWidget | None = None) -> None:
        QDockWidget.__init__(self, parent)
        self.ui = Ui_ThumbnailDock()
        self.ui.setupUi(self)
        self._setup_icons()
        self._setup_keyboard_shortcuts()

        self.model = None

    def _setup_icons(self) -> None:
        """Set up icons for actions."""
        # Toolbar
        self.ui.addPhotoAction.setIcon(QIcon(QIcon("src/preprocessor/icons/fugue16/image--plus.png")))
        self.ui.removePhotoAction.setIcon(QIcon(QIcon("src/preprocessor/icons/fugue16/image--minus.png")))


    def _setup_keyboard_shortcuts(self) -> None:
        """Set up keyboard shortcuts for actions."""
        # Toolbar
        self.ui.addPhotoAction.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_Equal)
        self.ui.removePhotoAction.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_Backspace)

    def update_thumbnails(self, photos: QListModel[PhotoModel]) -> None:
        """Update the thumbnails to match the given list of photos."""
        thumbnail_list: QListWidget = self.ui.thumbnailListWidget

        # Go through the list, removing photos that are no longer present and adding new ones,
        # while preserving order and minimizing changes to the list widget
        current_photos = [thumbnail_list.item(i).data(Qt.ItemDataRole.UserRole) for i in range(thumbnail_list.count())]
        current_photos_set = set(current_photos)
        new_photos_set = set(photos)
        removed = current_photos_set - new_photos_set
        added = new_photos_set - current_photos_set

        # Remove items corresponding to removed PhotoModel instances
        for photo in removed:
            # Find by stored PhotoModel in UserRole or fallback to matching filename
            found_index = None
            for i in range(thumbnail_list.count()):
                item = thumbnail_list.item(i)
                item_photo = item.data(Qt.ItemDataRole.UserRole)
                # Compare by identity first, then by basename of original filename
                if item_photo is photo:
                    found_index = i
                    break
                if photo.original_filename:
                    if item.text() == Path(photo.original_filename).name:
                        found_index = i
                        break
            if found_index is not None:
                # takeItem returns the removed QListWidgetItem; Qt will handle deletion by parent
                thumbnail_list.takeItem(found_index)

        # Insert items for added PhotoModel instances at the correct index to preserve order
        for photo in added:
            try:
                insert_index = photos.index(photo)
            except ValueError:
                insert_index = thumbnail_list.count()

            # Show basename as text; if there's an image file, load it as a thumbnail icon
            display_text = Path(photo.original_filename).name if photo.original_filename else ""
            item = QListWidgetItem(display_text)

            if photo.original_filename:
                pix = QPixmap(str(photo.original_filename))
                if not pix.isNull():
                    thumb = pix.scaled(QSize(120, 120), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    item.setIcon(QIcon(thumb))

            item.setData(Qt.ItemDataRole.UserRole, photo)
            # Insert at the position matching the project's photo index
            thumbnail_list.insertItem(insert_index, item)