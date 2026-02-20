import contextlib
import math
from collections.abc import Callable

from PySide6.QtCore import QPoint, Qt, QRect, QSize, QEvent
from PySide6.QtGui import QPixmap, QMouseEvent, QPainter, QPaintEvent, QPen
from PySide6.QtGui import QEnterEvent, QPainterPath, QPolygonF, QColor
from PySide6.QtWidgets import QWidget
from cv2.typing import MatLike

from preprocessor.model.photo_model import PhotoModel
from preprocessor.model.project_model import ProjectModel
from preprocessor.processing.undistort import undistort_photo
from preprocessor.processing.load_image import load_image
from preprocessor.gui.worker import Worker, start_worker


class PhotoEditorWidget(QWidget):
    """Widget for viewing and editing photos."""

    _mouse_position: QPoint | None
    """Current mouse position over the photo."""
    _pixmap: QPixmap | None
    """Current photo pixmap."""
    _photo: PhotoModel | None
    """Current photo model."""
    _drag_index: int | None
    """Index of corner being dragged (None when not dragging)."""
    _handle_radius: int
    """Visual radius for handles (in widget pixels)."""
    _edit_points: list[QPoint] | None
    """Working copy of points in widget coordinates while the user is editing."""
    _original_cv_img: MatLike | None
    """The original image loaded as an OpenCV/numpy array (if available)."""
    _undistorted_cv_img: MatLike | None
    """Last undistorted cv image (cached)."""
    _photo_signals_connected: bool
    """Whether we've connected model signals for the current photo."""
    _current_project: ProjectModel | None
    _current_undistort_worker: Worker | None

    def __init__(self, parent: QWidget | None = None) -> None:
        QWidget.__init__(self, parent)
        self._mouse_position = None
        self._pixmap = None
        self._photo = None

        self._drag_index = None
        self._handle_radius = 8

        # working copy used during editing (widget coordinates). None when not editing.
        self._edit_points = None

        # CV images (numpy arrays) used for undistortion
        self._original_cv_img = None
        self._undistorted_cv_img = None
        self._photo_signals_connected = False

        self.setMouseTracking(True)
        self._current_project = None
        self._current_undistort_worker = None

    def show_photo(self, photo: PhotoModel | None, project: ProjectModel) -> None:
        if photo is not None:
            original_path = project.get_absolute_path(photo.original_filename)
            # Load a QPixmap for fast rendering and also attempt to load a cv image
            self._pixmap = QPixmap(str(original_path))
            # Disconnect signals from previous photo (if any)
            try:
                if self._photo_signals_connected and self._photo is not None:
                    try:
                        self._photo.on_camera_matrix_changed.disconnect(self._on_camera_or_distortion_changed)
                    except Exception:
                        pass
                    try:
                        self._photo.on_distortion_coefficients_changed.disconnect(self._on_camera_or_distortion_changed)
                    except Exception:
                        pass
                    self._photo_signals_connected = False
            except Exception:
                # ignore disconnect errors
                pass

            self._photo = photo
            self._current_project = project

            # Try to load the CV image lazily (used for undistortion) using the project's loader
            try:
                self._original_cv_img = load_image(str(original_path))
            except Exception:
                self._original_cv_img = None

            # Connect signals from the model so we can react when camera or distortion change
            # First disconnect any previous connections
            try:
                # Connect to the new photo signals
                self._photo.on_camera_matrix_changed.connect(self._on_camera_or_distortion_changed)
                self._photo.on_distortion_coefficients_changed.connect(self._on_camera_or_distortion_changed)
                self._photo_signals_connected = True
            except Exception:
                # If connecting fails, ignore silently (signals may be different in tests)
                self._photo_signals_connected = False

            # Immediately apply undistortion if possible (async)
            self._apply_undistort_and_update()
        else:
            # Disconnect any previous signals and clear state
            try:
                if self._photo_signals_connected and self._photo is not None:
                    try:
                        self._photo.on_camera_matrix_changed.disconnect(self._on_camera_or_distortion_changed)
                    except Exception:
                        pass
                    try:
                        self._photo.on_distortion_coefficients_changed.disconnect(self._on_camera_or_distortion_changed)
                    except Exception:
                        pass
            except Exception:
                pass
            self._pixmap = None
            self._photo = None
            # Clear any stored cv images & signal flags
            self._original_cv_img = None
            self._undistorted_cv_img = None
            self._photo_signals_connected = False
        # Stop any active dragging when switching photos
        self._drag_index = None
        # discard any unfinished edit when switching photos
        self._edit_points = None
        self.update()

    def _on_camera_or_distortion_changed(self, *args: object, **kwargs: object) -> None:
        """Handler called when the photo camera matrix or distortion coefficients change.
        Applies undistortion to the currently displayed image and updates the pixmap.
        """
        self._apply_undistort_and_update()

    def _apply_undistort_and_update(self) -> None:
        """Apply undistort() to the loaded CV image and update the displayed QPixmap.
        Falls back to the original QPixmap if undistortion isn't possible.
        """
        if self._photo is None:
            return

        # Need an original CV image and camera/distortion parameters
        if self._original_cv_img is None:
            # Nothing to do; keep existing pixmap
            self.update()
            return

        cam = getattr(self._photo, "camera_matrix", None)
        dist = getattr(self._photo, "distortion_coefficients", None)

        if cam is None or dist is None:
            # No parameters: show original
            self._undistorted_cv_img = None
            # ensure pixmap matches original file (no-op if same)
            self.update()
            return

        # Start asynchronous undistortion for the current photo (non-blocking)
        try:
            # Start async undistort; fallback to sync if starting fails
            self._start_undistort_for_current()
        except Exception:
            # Fall back to synchronous undistortion if async start fails
            try:
                from preprocessor.processing.fix_lens_distortion import undistort
                from PySide6.QtGui import QImage

                und = undistort(self._original_cv_img, cam, list(dist))
                if und is None:
                    raise RuntimeError("undistort returned None")

                # und is in BGR/BGRA ordering (OpenCV). Convert to RGB/RGBA for QImage
                import cv2

                if und.ndim == 3 and und.shape[2] == 3:
                    rgb = cv2.cvtColor(und, cv2.COLOR_BGR2RGB).copy()
                    h, w, ch = rgb.shape
                    bytes_per_line = ch * w
                    qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).copy()
                elif und.ndim == 3 and und.shape[2] == 4:
                    rgba = cv2.cvtColor(und, cv2.COLOR_BGRA2RGBA).copy()
                    h, w, ch = rgba.shape
                    bytes_per_line = ch * w
                    qimg = QImage(rgba.data, w, h, bytes_per_line, QImage.Format.Format_RGBA8888).copy()
                else:
                    gray = und.copy()
                    h, w = gray.shape
                    qimg = QImage(gray.data, w, h, w, QImage.Format.Format_Grayscale8).copy()

                self._pixmap = QPixmap.fromImage(qimg)
                self._undistorted_cv_img = und
                self.update()
            except Exception:
                self._undistorted_cv_img = None
                self.update()

    def get_processing_image(self) -> MatLike | None:
        """Return a cv2 image to use for processing (undistorted if available).

        Returns the undistorted image if we've successfully computed it, otherwise
        returns the original cv image if available, otherwise None.
        """
        if self._undistorted_cv_img is not None:
            return self._undistorted_cv_img
        return self._original_cv_img

    def _current_pixmap_info(self) -> tuple[float, QPoint, QSize]:
        """
        Return (ratio, top_left_offset, scaled_size) for the currently-loaded pixmap
        relative to widget coordinates. If no pixmap is present, returns ratio=1.0,
        offset=(0,0) and size equal to the widget size.
        """
        if self._pixmap is None or self._pixmap.width() == 0 or self._pixmap.height() == 0:
            return 1.0, QPoint(0, 0), QSize(self.width(), self.height())
        ratio = min(self.width() / self._pixmap.width(), self.height() / self._pixmap.height())
        scaled_w = round(self._pixmap.width() * ratio)
        scaled_h = round(self._pixmap.height() * ratio)
        # keep top-left at (0,0) (same behavior as the painter)
        offset = QPoint(0, 0)
        return ratio, offset, QSize(scaled_w, scaled_h)

    def _image_to_widget_point(self, x: float, y: float) -> QPoint:
        """Map a point from image (model) coordinates to widget coordinates."""
        ratio, offset, _ = self._current_pixmap_info()
        return QPoint(round(x * ratio + offset.x()), round(y * ratio + offset.y()))

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
        If an edit is in progress, return the working copy instead.
        """
        if self._edit_points is not None:
            return list(self._edit_points)
        if self._photo is None or self._photo.quadrat_corners is None:
            return []
        return [self._image_to_widget_point(x, y) for x, y in self._photo.quadrat_corners]

    def _write_widget_points(self, pts: list[QPoint] | None) -> None:
        """Write a list of QPoint (or None) back into the PhotoModel as list of floats (image coords) or None.
        Converts the widget coordinates (mouse positions) into image coordinates using the current scale.
        """
        if self._photo is None:
            return
        if not pts:
            self._photo.quadrat_corners = None
        else:
            # Ensure a stable ordering before storing so polygon stays simple
            if len(pts) >= 3:
                pts = self._order_points_by_angle(pts)
            img_pts = [self._widget_to_image_point(p) for p in pts]
            self._photo.quadrat_corners = [(float(x), float(y)) for x, y in img_pts]

    def paintEvent(self, _event: QPaintEvent) -> None:
        painter = QPainter(self)

        # Draw the photo pixmap, scaled to fit the widget
        if self._pixmap is not None:
            _ratio, offset, size = self._current_pixmap_info()
            scaled_pixmap = self._pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio)
            pixmap_rect = QRect(offset, size)
            painter.drawPixmap(pixmap_rect, scaled_pixmap)

        # Determine quadrat points from model or working copy (as widget points)
        qcorners = self._widget_points()

        # Draw shaded overlay outside the quadrat (if any)
        if qcorners is not None and len(qcorners) >= 1:
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
            for a, b in zip(qcorners, [*qcorners[1:], qcorners[0]], strict=False):
                painter.drawLine(a, b)

        # Draw handles for each corner (so they are visible and draggable)
        pts = qcorners or []
        if pts:
            for _i, p in enumerate(pts):
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
            # fmt: off
            length = 10                             # Arm length, in pixels
            gap = 5                                 # Gap size, in pixels
            width = 2                               # Line width, in pixels
            border = 1                              # Border width, in pixels
            border_color = Qt.GlobalColor.white     # Border color
            line_color = Qt.GlobalColor.red         # Line color
            # fmt: on
            x = self._mouse_position.x()
            y = self._mouse_position.y()

            def draw_crosshair() -> None:
                painter.drawLine(QPoint(x - gap - length, y), QPoint(x - gap, y))
                painter.drawLine(QPoint(x + gap, y), QPoint(x + gap + length, y))
                painter.drawLine(QPoint(x, y - gap - length), QPoint(x, y - gap))
                painter.drawLine(QPoint(x, y + gap), QPoint(x, y + gap + length))

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
                # Begin dragging an existing point: make a working copy if needed
                if self._edit_points is None:
                    self._edit_points = self._widget_points()
                self._drag_index = hit
            else:
                # Add new point if less than 4 exist, and start editing it (do not persist yet)
                pts = self._widget_points()
                if len(pts) < 4:
                    # initialize working copy if not present
                    if self._edit_points is None:
                        self._edit_points = pts
                    self._edit_points.append(event.pos())
                    self._drag_index = len(self._edit_points) - 1
            self._mouse_position = event.pos()
            self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            hit = self._find_handle_index(event.pos())
            if hit is not None:
                # Remove an existing point under the cursor immediately (right-click is immediate)
                pts = self._widget_points()
                del pts[hit]
                # persist removal immediately
                self._write_widget_points(pts if pts else None)
                # stop any drag if removing dragged point
                if self._drag_index == hit:
                    self._drag_index = None
                # discard any working copy after committing
                self._edit_points = None
                self.update()
            else:
                self._mouse_position = event.pos()
                self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self._mouse_position = event.pos()
        if self._drag_index is not None and self._photo is not None:
            # Dragging: update the working copy only (do not persist yet)
            if self._edit_points is None:
                self._edit_points = self._widget_points()
            pts = self._edit_points
            if 0 <= self._drag_index < len(pts):
                pts[self._drag_index] = event.pos()
            # do not call _write_widget_points here
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        # Stop dragging and persist any working edits
        if self._edit_points is not None:
            # commit working copy into the model
            self._write_widget_points(self._edit_points if self._edit_points else None)
            # discard working copy after commit
            self._edit_points = None
        self._drag_index = None
        self._mouse_position = event.pos()
        self.update()

    def enterEvent(self, event: QEnterEvent) -> None:
        """Hide the OS mouse cursor while inside the editor."""
        self.setCursor(Qt.CursorShape.BlankCursor)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        """Restore the OS mouse cursor when leaving the editor."""
        # If an edit was in progress, commit it when dragging is ended by leaving
        if self._edit_points is not None:
            self._write_widget_points(self._edit_points if self._edit_points else None)
            self._edit_points = None
        self.unsetCursor()
        self._mouse_position = None
        self._drag_index = None  # Stop dragging (if any)
        self.update()
        super().leaveEvent(event)

    @staticmethod
    def _order_points_by_angle(pts: list[QPoint]) -> list[QPoint]:
        """Return points sorted by angle around their centroid (counter-clockwise).
        This ordering yields a simple polygon (no self intersections) for small point sets.
        """
        if not pts:
            return pts
        cx = sum(p.x() for p in pts) / len(pts)
        cy = sum(p.y() for p in pts) / len(pts)
        return sorted(pts, key=lambda p: math.atan2(p.y() - cy, p.x() - cx))

    def undistort_photo_async(self, photo: PhotoModel, project: ProjectModel, result_callback: Callable[[object], None] | None = None) -> None:
        """Start an asynchronous undistortion for the specified photo/project.

        The result_callback (if provided) will be called with one argument: the undistorted cv image (or None on failure).
        This method can be used to batch undistort photos that are not currently displayed.
        """
        # Create a worker to run the undistort in background
        worker = Worker(undistort_photo, photo, project)

        def _on_result(result: object) -> None:
            if result_callback is not None:
                with contextlib.suppress(Exception):
                    result_callback(result)

        def _on_error(err: tuple) -> None:
            # Pass None to callback on error
            if result_callback is not None:
                with contextlib.suppress(Exception):
                    result_callback(None)

        worker.signals.result.connect(_on_result)
        worker.signals.error.connect(_on_error)
        start_worker(worker)

    def _start_undistort_for_current(self) -> None:
        """Internal: start async undistort for the currently shown photo and update the widget when done."""
        if self._photo is None or self._current_project is None:
            return

        # If a previous worker is running, we won't cancel it here; just start another
        worker = Worker(undistort_photo, self._photo, self._current_project)
        self._current_undistort_worker = worker

        def _on_result(result: MatLike | None) -> None:
            try:
                if result is None:
                    self._undistorted_cv_img = None
                else:
                    self._undistorted_cv_img = result
                    # update pixmap from result on the main thread
                    try:
                        from PySide6.QtGui import QImage

                        und = result
                        # Result is in BGR/BGRA ordering (OpenCV). Convert to RGB/RGBA for QImage
                        import cv2

                        if und.ndim == 3 and und.shape[2] == 3:
                            rgb = cv2.cvtColor(und, cv2.COLOR_BGR2RGB).copy()
                            h, w, ch = rgb.shape
                            bytes_per_line = ch * w
                            qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).copy()
                        elif und.ndim == 3 and und.shape[2] == 4:
                            rgba = cv2.cvtColor(und, cv2.COLOR_BGRA2RGBA).copy()
                            h, w, ch = rgba.shape
                            bytes_per_line = ch * w
                            qimg = QImage(rgba.data, w, h, bytes_per_line, QImage.Format.Format_RGBA8888).copy()
                        else:
                            gray = und.copy()
                            h, w = gray.shape
                            qimg = QImage(gray.data, w, h, w, QImage.Format.Format_Grayscale8).copy()
                        self._pixmap = QPixmap.fromImage(qimg)
                    except Exception:
                        # if conversion fails, leave pixmap as-is
                        pass
            finally:
                # Clear worker ref and repaint
                self._current_undistort_worker = None
                self.update()

        def _on_error(err: tuple) -> None:
            self._undistorted_cv_img = None
            self._current_undistort_worker = None
            self.update()

        worker.signals.result.connect(_on_result)
        worker.signals.error.connect(_on_error)
        start_worker(worker)
