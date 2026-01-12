from typing import Sequence, Optional, Any
from dataclasses import dataclass

from PySide6.QtCore import Signal, QObject


@dataclass
class ThumbnailItem:
    path: str
    result: Optional[Any] = None  # QuadratDetectionResult | None (use Any to avoid tight coupling)


class ThumbnailListModel(QObject):
    on_changed: Signal = Signal()

    _items: list[ThumbnailItem] = []
    on_image_paths_changed: Signal = Signal()

    @property
    def image_paths(self) -> list[str]:
        # Return paths in order
        return [item.path for item in self._items]

    @image_paths.setter
    def image_paths(self, paths: list[str]) -> None:
        if paths == self.image_paths:
            return
        # Preserve existing results for paths that remain; append new paths with result=None
        new_items: list[ThumbnailItem] = []
        existing_map = {item.path: item for item in self._items}
        for p in paths:
            if p in existing_map:
                new_items.append(existing_map[p])
            else:
                new_items.append(ThumbnailItem(path=p, result=None))
        self._items = new_items
        self.on_image_paths_changed.emit()
        self.on_changed.emit()

    def __init__(self, image_paths: Sequence[str] | None = None, parent: QObject | None = None):
        super().__init__(parent)
        self._items = [ThumbnailItem(path=p, result=None) for p in (image_paths or [])]

    def get_result_for_path(self, path: str) -> Optional[Any]:
        for item in self._items:
            if item.path == path:
                return item.result
        return None

    def set_result_for_path(self, path: str, result: Any) -> None:
        for item in self._items:
            if item.path == path:
                item.result = result
                self.on_changed.emit()
                return
        # If not present, append new item with result
        self._items.append(ThumbnailItem(path=path, result=result))
        self.on_image_paths_changed.emit()
        self.on_changed.emit()
