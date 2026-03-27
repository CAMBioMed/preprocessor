from PySide6.QtCore import Qt, QSize, Signal, QPoint
from PySide6.QtGui import QIcon, QPixmap, QAction, QKeySequence
from PySide6.QtWidgets import QDockWidget, QWidget, QListWidget, QListWidgetItem, QMenu

from preprocessor.gui.ui_thumbnail_dock import Ui_ThumbnailDock
from preprocessor.gui.utils import icon_from_resource
from preprocessor.model.project_model import ProjectModel
from preprocessor.model.qlistmodel import QListModel
from preprocessor.model.photo_model import PhotoModel


class ThumbnailDockWidget(QDockWidget):
    ui: Ui_ThumbnailDock

    on_add_photos_action: Signal = Signal()
    on_remove_photos_action: Signal = Signal(object)
    on_selection_changed: Signal = Signal(object)  # Signal(list[PhotoModel])
    on_item_double_clicked: Signal = Signal(object)  # Signal(PhotoModel | None)
    on_apply_parameters_to_selected: Signal = Signal(object)  # Signal(list[PhotoModel])
    on_set_metadata_to_selected: Signal = Signal(object)  # Signal(list[PhotoModel])

    def __init__(self, parent: QWidget | None = None) -> None:
        QDockWidget.__init__(self, parent)
        self.ui = Ui_ThumbnailDock()
        self.ui.setupUi(self)
        self._setup_icons()
        self._setup_keyboard_shortcuts()
        self._connect_signals()

        self.model = None

    def _setup_icons(self) -> None:
        """Set up icons for actions."""
        # Toolbar
        self.ui.addPhotoAction.setIcon(icon_from_resource("icons/fuguex2/image--plus.png"))
        self.ui.removePhotoAction.setIcon(icon_from_resource("icons/fuguex2/image--minus.png"))

    def _setup_keyboard_shortcuts(self) -> None:
        """Set up keyboard shortcuts for actions."""
        # Toolbar
        # Use explicit QKeySequence strings for cross-platform clarity
        self.ui.addPhotoAction.setShortcut(QKeySequence("Ctrl+="))
        self.ui.removePhotoAction.setShortcut(QKeySequence("Ctrl+Backspace"))

    def _connect_signals(self) -> None:
        """Connect UI signals to internal handlers."""
        self.ui.addPhotoAction.triggered.connect(self._handle_add_photos_action)
        self.ui.removePhotoAction.triggered.connect(self._handle_remove_photos_action)
        self.ui.thumbnailListWidget.itemDoubleClicked.connect(self._handle_item_double_clicked)
        self.ui.thumbnailListWidget.itemSelectionChanged.connect(self._handle_selection_changed)

        # Enable custom context menu on the list widget and handle right-clicks
        self.ui.thumbnailListWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.thumbnailListWidget.customContextMenuRequested.connect(self._handle_context_menu)

    def _handle_add_photos_action(self) -> None:
        self.on_add_photos_action.emit()

    def _handle_remove_photos_action(self) -> None:
        selected_items = self.ui.thumbnailListWidget.selectedItems()
        selected_photos = [
            item.data(Qt.ItemDataRole.UserRole)
            for item in selected_items
            if item.data(Qt.ItemDataRole.UserRole) is not None
        ]
        self.on_remove_photos_action.emit(selected_photos)

    def _handle_selection_changed(self) -> None:
        selected_items = self.ui.thumbnailListWidget.selectedItems()
        selected_photos = [
            item.data(Qt.ItemDataRole.UserRole)
            for item in selected_items
            if item.data(Qt.ItemDataRole.UserRole) is not None
        ]
        self.on_selection_changed.emit(selected_photos)

    def _handle_item_double_clicked(self, item: QListWidgetItem) -> None:
        model: PhotoModel | None = item.data(Qt.ItemDataRole.UserRole)
        self.on_item_double_clicked.emit(model)

    def _handle_context_menu(self, pos: QPoint) -> None:
        """Show a context menu when the user right-clicks the thumbnail list."""
        # Build list of selected photos
        selected_items = self.ui.thumbnailListWidget.selectedItems()
        selected_photos = [
            item.data(Qt.ItemDataRole.UserRole)
            for item in selected_items
            if item.data(Qt.ItemDataRole.UserRole) is not None
        ]

        if not selected_photos:
            # Nothing selected; don't show context menu
            return

        # Create menu and actions
        menu = QMenu(self)

        apply_parameters_action = QAction("Apply Parameters...", self)
        apply_parameters_action.triggered.connect(
            lambda: self._handle_apply_parameters_to_selected_action(selected_photos)
        )
        menu.addAction(apply_parameters_action)

        # Connect action
        set_metadata_action = QAction("Edit Metadata...", self)
        set_metadata_action.triggered.connect(lambda: self._handle_set_metadata_to_selected_action(selected_photos))
        menu.addAction(set_metadata_action)

        # Show menu at the global position
        global_pos = self.ui.thumbnailListWidget.mapToGlobal(pos)
        menu.exec(global_pos)

    def _handle_apply_parameters_to_selected_action(self, selected_photos: list[PhotoModel]) -> None:
        """Emit signal to indicate user requested 'Apply to all' for the selected photos."""
        self.on_apply_parameters_to_selected.emit(selected_photos)

    def _handle_set_metadata_to_selected_action(self, selected_photos: list[PhotoModel]) -> None:
        """Emit signal to indicate user requested 'Set metadata to all' for the selected photos."""
        self.on_set_metadata_to_selected.emit(selected_photos)

    def update_thumbnails(self, photos: QListModel[PhotoModel], project: ProjectModel) -> None:
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
                if item_photo is photo or item.text() == photo.name:
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
            display_text = photo.name
            item = QListWidgetItem(display_text)

            original_path = photo.original_filename
            pix = QPixmap(str(original_path))
            if not pix.isNull():
                thumb = pix.scaled(
                    QSize(120, 120),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                item.setIcon(QIcon(thumb))

            item.setData(Qt.ItemDataRole.UserRole, photo)
            # Insert at the position matching the project's photo index
            thumbnail_list.insertItem(insert_index, item)
