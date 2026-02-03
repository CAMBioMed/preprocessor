from pathlib import Path

from PySide6.QtCore import QPoint, Qt, QRect, QSize, QEvent
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

        # index of corner being dragged (None when not dragging)
        self._drag_index: int | None = None
        # visual radius for handles (in widget pixels)
        self._handle_radius = 8

        self.setMouseTracking(True)

    def show_photo(self, photo: PhotoModel | None) -> None:
        if photo is not None:
            self._pixmap = QPixmap(str(photo.original_filename))
            self._photo = photo
        else:
            self._pixmap = None
            self._photo = None
        # stop any active drag when switching photos
        self._drag_index = None
        self.update()

    def _current_pixmap_info(self) -> tuple[float, QPoint, QSize]:
        """
        Return (ratio, top_left_offset, scaled_size) for the currently-loaded pixmap
        relative to widget coordinates. If no pixmap is present, returns ratio=1.0,
        offset=(0,0) and size equal to the widget size.
        """
        if self._pixmap is None or self._pixmap.width() == 0 or self._pixmap.height() == 0:
            return 1.0, QPoint(0, 0), QSize(self.width(), self.height())
        ratio = min(self.width() / self._pixmap.width(), self.height() / self._pixmap.height())
        scaled_w = int(round(self._pixmap.width() * ratio))
        scaled_h = int(round(self._pixmap.height() * ratio))
        # keep top-left at (0,0) (same behavior as the painter)
        offset = QPoint(0, 0)
        return ratio, offset, QSize(scaled_w, scaled_h)

    def _image_to_widget_point(self, x: float, y: float) -> QPoint:
        """Map a point from image (model) coordinates to widget coordinates."""
        ratio, offset, _ = self._current_pixmap_info()
        return QPoint(int(round(x * ratio + offset.x())), int(round(y * ratio + offset.y())))

    def _widget_to_image_point(self, pt: QPoint) -> tuple[float, float]:
        """Map a QPoint in widget coordinates back to image (model) coordinates."""
        ratio, offset, _ = self._current_pixmap_info()
        if ratio == 0:
            return float(pt.x()), float(pt.y())
        ix = (pt.x() - offset.x()) / ratio
        iy = (pt.y() - offset.y()) / ratio
        return float(ix), float(iy)

    def _widget_points(self) -> list[QPoint]:
        """Return quadrat corners as widget QPoint instances (empty list if none).
        The stored PhotoModel.quadrat_corners are interpreted as image coordinates
        and are scaled to match the rendered (scaled) pixmap.
        """
        if self._photo is None or self._photo.quadrat_corners is None:
            return []
        return [self._image_to_widget_point(x, y) for x, y in self._photo.quadrat_corners]

    def _write_widget_points(self, pts: list[QPoint] | None) -> None:
        """Write a list of QPoint (or None) back into the PhotoModel as tuple of floats (image coords) or None.
        Converts the widget coordinates (mouse positions) into image coordinates using the current scale.
        """
        if self._photo is None:
            return
        if not pts:
            self._photo.quadrat_corners = None
        else:
            img_pts = [self._widget_to_image_point(p) for p in pts]
            self._photo.quadrat_corners = tuple((float(x), float(y)) for x, y in img_pts)

    def paintEvent(self, _event: QPaintEvent) -> None:
        painter = QPainter(self)

        # Draw the photo pixmap, scaled to fit the widget
        if self._pixmap is not None:
            ratio, offset, size = self._current_pixmap_info()
            scaled_pixmap = self._pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio)
            pixmap_rect = QRect(offset, size)
            painter.drawPixmap(pixmap_rect, scaled_pixmap)

        # Determine quadrat points from model (as widget points)
        if self._photo is not None and self._photo.quadrat_corners is not None:
            qcorners = [self._image_to_widget_point(x, y) for x, y in self._photo.quadrat_corners]
        else:
            qcorners = None

        # Draw shaded overlay outside the quadrat (if any)
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
        if qcorners is not None and len(qcorners) >= 2:
            painter.setPen(QPen(Qt.GlobalColor.green, 2, Qt.PenStyle.SolidLine))
            for a, b in zip(qcorners, qcorners[1:] + [qcorners[0]]):
                painter.drawLine(a, b)

        # Draw handles for each corner (so they are visible and draggable)
        pts = qcorners or []
        if pts:
            for i, p in enumerate(pts):
                # outer border
                painter.setPen(QPen(Qt.GlobalColor.white, 2))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                r = self._handle_radius
                painter.drawEllipse(p, r, r)
                # inner fill
                painter.setPen(QPen(Qt.GlobalColor.black, 1))
                painter.setBrush(QColor(255, 255, 255))
                painter.drawEllipse(p, r - 3, r - 3)

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

    def _find_handle_index(self, pos: QPoint) -> int | None:
        """Return index of handle under pos, or None."""
        pts = self._widget_points()
        r = self._handle_radius
        r2 = r * r
        for i, p in enumerate(pts):
            dx = p.x() - pos.x()
            dy = p.y() - pos.y()
            if dx * dx + dy * dy <= r2:
                return i
        return None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self._photo is None:
            self._mouse_position = event.pos()
            self.update()
            return

        if event.button() == Qt.MouseButton.LeftButton:
            hit = self._find_handle_index(event.pos())
            if hit is not None:
                # Begin dragging an existing point
                self._drag_index = hit
            else:
                # Add new point if less than 4 exist, and start dragging it
                pts = self._widget_points()
                if len(pts) < 4:
                    pts.append(event.pos())
                    self._write_widget_points(pts)
                    self._drag_index = len(pts) - 1
            self._mouse_position = event.pos()
            self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            hit = self._find_handle_index(event.pos())
            if hit is not None:
                # Remove an existing point under the cursor
                pts = self._widget_points()
                del pts[hit]
                self._write_widget_points(pts if pts else None)
                # stop any drag if removing dragged point
                if self._drag_index == hit:
                    self._drag_index = None
                self.update()
            else:
                self._mouse_position = event.pos()
                self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self._mouse_position = event.pos()
        if self._drag_index is not None and self._photo is not None:
            # Dragging
            pts = self._widget_points()
            if 0 <= self._drag_index < len(pts):
                pts[self._drag_index] = event.pos()
                self._write_widget_points(pts)
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        # Stop dragging
        self._drag_index = None
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
        self._drag_index = None     # Stop dragging (if any)
        self.update()
        super().leaveEvent(event)
