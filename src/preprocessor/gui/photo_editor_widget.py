from pathlib import Path

from PySide6.QtCore import QPoint, Qt, QRect
from PySide6.QtGui import QPixmap, QMouseEvent, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QWidget

from preprocessor.model.photo_model import PhotoModel


class PhotoEditorWidget(QWidget):
    """Widget for viewing and editing photos."""

    _mouse_position: QPoint | None
    """Current mouse position over the photo."""
    _pixmap: QPixmap | None
    """Current photo pixmap."""

    def __init__(self, parent: QWidget | None = None) -> None:
        QWidget.__init__(self, parent)
        self._mouse_position = None
        self._pixmap = None

        self.setMouseTracking(True)

    def show_photo(self, photo: PhotoModel | None) -> None:
        if photo is not None:
            self._pixmap = QPixmap(str(photo.original_filename))
        else:
            self._pixmap = None
        self.update()

    def paintEvent(self, _event: QPaintEvent) -> None:
        painter = QPainter(self)

        if self._pixmap is not None:
            ratio = min(1.0 * self.width() / self._pixmap.width(), 1.0 * self.height() / self._pixmap.height())
            size = self._pixmap.size() * ratio
            scaled_pixmap = self._pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio)
            painter.drawPixmap(QRect(QPoint(), size), scaled_pixmap)

        if self._mouse_position is not None:
            painter.setPen(QPen(Qt.GlobalColor.red, 15, Qt.PenStyle.SolidLine))
            painter.drawEllipse(self._mouse_position, 15, 15)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self._mouse_position = event.pos()
        self.update()
