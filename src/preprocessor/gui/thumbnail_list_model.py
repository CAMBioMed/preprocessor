from typing import Sequence

from PySide6.QtCore import Signal, QObject


class ThumbnailListModel(QObject):
    on_changed: Signal = Signal()

    _image_paths: list[str] = []
    on_image_paths_changed: Signal = Signal()

    @property
    def image_paths(self) -> list[str]:
        return list(self._image_paths)  # Safety copy

    @image_paths.setter
    def image_paths(self, paths: list[str]) -> None:
        if paths == self._image_paths:
            return
        self._image_paths = list(paths)
        self.on_image_paths_changed.emit()
        self.on_changed.emit()

    def __init__(self, image_paths: Sequence[str] | None = None, parent: QObject | None = None):
        super().__init__(parent)
        self._image_paths = list(image_paths) if image_paths else []
