from PySide6.QtCore import QRect, QPoint, Qt
from PySide6.QtGui import QPainter, QPen, QPixmap, QMouseEvent, QPaintEvent
from PySide6.QtWidgets import QWidget


class QImageEditor(QWidget):

    position: QPoint | None
    _pixmap: QPixmap | None

    @property
    def pixmap(self) -> QPixmap | None:
        return self._pixmap

    @pixmap.setter
    def pixmap(self, pixmap: QPixmap | None) -> None:
        self._pixmap = pixmap
        self.update()

    _message: str | None

    @property
    def message(self) -> str | None:
        return self._message

    @message.setter
    def message(self, message: str | None) -> None:
        self._message = message
        self.update()

    def __init__(self, parent: QWidget | None = None) -> None:
        QWidget.__init__(self, parent=parent)
        self._pixmap = None
        self._message = None
        self.position = None
        self.setMouseTracking(True)

    def paintEvent(self, _event: QPaintEvent) -> None:
        painter = QPainter(self)

        if self._pixmap:
            ratio = min(1.0 * self.width() / self._pixmap.width(), 1.0 * self.height() / self._pixmap.height())
            size = self._pixmap.size() * ratio
            scaled_pixmap = self._pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio)
            painter.drawPixmap(QRect(QPoint(), size), scaled_pixmap)

        if self._message:
            painter.drawText(10, 30, self._message or "")

        if self.position:
            painter.setPen(QPen(Qt.GlobalColor.red, 15, Qt.PenStyle.SolidLine))
            painter.drawEllipse(self.position, 15, 15)

    def mouseMoveEvent(self, event : QMouseEvent) -> None:
        self.position = event.pos()
        self.update()
