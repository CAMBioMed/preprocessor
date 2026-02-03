from pathlib import Path

from PySide6.QtCore import QPoint, Qt, QRect, QEvent
from PySide6.QtGui import QPixmap, QMouseEvent, QPainter, QPaintEvent, QPen, QEnterEvent, QPainterPath, QPolygonF, QColor
from PySide6.QtWidgets import QWidget

from preprocessor.model.photo_model import PhotoModel


class PhotoEditorWidget(QWidget):
    """Widget for viewing and editing photos."""

    _mouse_position: QPoint | None
    """Current mouse position over the photo."""
    _pixmap: QPixmap | None
    """Current photo pixmap."""
    _photo: PhotoModel | None
    """Current photo model."""

    def __init__(self, parent: QWidget | None = None) -> None:
        QWidget.__init__(self, parent)
        self._mouse_position = None
        self._pixmap = None
        self._photo = None

        self.setMouseTracking(True)

    def show_photo(self, photo: PhotoModel | None) -> None:
        if photo is not None:
            self._pixmap = QPixmap(str(photo.original_filename))
            self._photo = photo
        else:
            self._pixmap = None
            self._photo = None
        self.update()

    def paintEvent(self, _event: QPaintEvent) -> None:
        painter = QPainter(self)

        # Draw the photo pixmap, scaled to fit the widget
        if self._pixmap is not None:
            ratio = min(1.0 * self.width() / self._pixmap.width(), 1.0 * self.height() / self._pixmap.height())
            size = self._pixmap.size() * ratio
            scaled_pixmap = self._pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio)
            pixmap_rect = QRect(QPoint(), size)
            painter.drawPixmap(pixmap_rect, scaled_pixmap)

        # Draw a shaded overlay outside the quadrat (if any)
        qcorners: list[QPoint] | None = None
        if self._photo is not None and self._photo.quadrat_corners is not None:
            corners = self._photo.quadrat_corners
            qcorners = [QPoint(int(round(x)), int(round(y))) for x, y in corners]

        # Draw a shaded overlay outside the quadrat (if any)
        if qcorners is not None:
            path = QPainterPath()
            path.addRect(self.rect())
            poly = QPolygonF(qcorners)
            path.addPolygon(poly)
            path.setFillRule(Qt.FillRule.OddEvenFill)
            painter.save()
            painter.setPen(Qt.PenStyle.NoPen)
            painter.fillPath(path, QColor(0, 0, 0, 100))  # semi-transparent black
            painter.restore()

        # Draw the quadrat outline (if any) on top of the shading
        if qcorners is not None:
            painter.setPen(QPen(Qt.GlobalColor.green, 2, Qt.PenStyle.SolidLine))
            painter.drawLine(qcorners[0], qcorners[1])
            painter.drawLine(qcorners[1], qcorners[2])
            painter.drawLine(qcorners[2], qcorners[3])
            painter.drawLine(qcorners[3], qcorners[0])

        # Draw a crosshair centered at the mouse position (drawn last so it's visible)
        if self._mouse_position is not None:
            length = 10                             # Arm length, in pixels
            offset = 5                              # Gap size, in pixels
            width = 2                               # Line width, in pixels
            border = 1                              # Border width, in pixels
            border_color = Qt.GlobalColor.white     # Border color
            line_color = Qt.GlobalColor.red         # Line color
            x = self._mouse_position.x()
            y = self._mouse_position.y()

            def draw_crosshair() -> None:
                painter.drawLine(QPoint(x - offset - length, y), QPoint(x - offset, y))
                painter.drawLine(QPoint(x + offset, y), QPoint(x + offset + length, y))
                painter.drawLine(QPoint(x, y - offset - length), QPoint(x, y - offset))
                painter.drawLine(QPoint(x, y + offset), QPoint(x, y + offset + length))

            painter.setPen(QPen(border_color, width + border * 2, Qt.PenStyle.SolidLine))
            draw_crosshair()

            painter.setPen(QPen(line_color, width, Qt.PenStyle.SolidLine))
            draw_crosshair()



    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self._mouse_position = event.pos()
        self.update()

    def enterEvent(self, event: QEnterEvent) -> None:
        """Hide the OS mouse cursor while inside the editor."""
        self.setCursor(Qt.CursorShape.BlankCursor)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        """Restore the OS mouse cursor when leaving the editor."""
        self.unsetCursor()
        self._mouse_position = None
        self.update()
        super().leaveEvent(event)
