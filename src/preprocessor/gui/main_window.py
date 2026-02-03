import logging
import signal
import sys
from typing import cast, Any

import cv2
from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QSettings, QByteArray, QTimer, Slot, Signal, QCoreApplication
from PySide6.QtGui import QAction, QIcon, QCloseEvent, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QWidget,
    QFileDialog, QDockWidget, QListWidget, QVBoxLayout, QGridLayout, QProgressDialog,
)
from cv2.typing import MatLike

from preprocessor.gui.about_dialog import show_about_dialog
from preprocessor.gui.hsv_threshold_widget import HSVThresholdWidget
from preprocessor.gui.image_editor import QImageEditor
from preprocessor.gui.main_window2 import MainWindow2
from preprocessor.gui.main_window_model import MainWindowModel
from preprocessor.gui.properties_dock_widget import PropertiesDockWidget
from preprocessor.gui.thumbnail_list_widget import ThumbnailListWidget
from preprocessor.processing.detect_quadrat import detect_quadrat, QuadratDetectionResult
from preprocessor.processing.fix_perspective import fix_perspective
from preprocessor.processing.load_image import load_image
from preprocessor.processing.params import QuadratDetectionParams
from preprocessor._version import __version__
from preprocessor.gui.worker import Worker, WorkerManager

from qimage2ndarray import array2qimage

from preprocessor.processing.save_image import save_image

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""

    model: MainWindowModel

    properties_dock: PropertiesDockWidget
    """The dock widget showing properties."""
    thumbnail_dock: ThumbnailListWidget
    """The dock widget showing image thumbnails."""
    central_widget: QImageEditor
    """The central widget showing the image."""
    _debounce_timer: QTimer
    """Timer for debouncing image processing parameter changes."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("CAMBioMed Preprocessor")
        self.resize(400, 200)
        self.settings = QSettings("CAMBioMed", "Preprocessor")

        self.create_debounce_timer()

        self.create_menu()
        self.create_toolbar()
        self.create_central_widget()
        self.create_properties_dock()
        self.create_thumbnail_list()
        self.create_statusbar()

        self.model = MainWindowModel()
        # FIXME: How to get the PropertiesDockModel into the widget?
        self._connect_signals()

        self.read_settings()

    def _connect_signals(self) -> None:
        # TODO
        pass

    def create_debounce_timer(self) -> None:
        debounce_interval_ms = 150  # milliseconds
        self._debounce_timer = QtCore.QTimer(self)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.setInterval(debounce_interval_ms)
        self._debounce_timer.timeout.connect(lambda: self._schedule_processing(self._current_image_path))

    def _on_parameter_change(self) -> None:
        # Start the timer to debounce rapid parameter changes
        # If the timer is already running, it will be restarted
        self._debounce_timer.start()

    def create_menu(self) -> None:
        """Create the main window menu."""
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")

        open_action = QAction("&Open...", self)
        open_action.setStatusTip("Open an image")
        open_action.triggered.connect(self.on_file_open)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        file_menu.addAction(open_action)

        save_action = QAction("&Save...", self)
        save_action.setStatusTip("Save the processed image")
        save_action.triggered.connect(self.on_file_save)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        file_menu.addAction(save_action)

        save_all_action = QAction("Save &All...", self)
        save_all_action.setStatusTip("Save all processed images")
        save_all_action.triggered.connect(self.on_file_save_all)
        file_menu.addAction(save_all_action)

        exit_action = QAction("&Exit", self)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.setStatusTip("Show the About dialog")
        about_action.triggered.connect(self.on_help_about)
        help_menu.addAction(about_action)

    view_original_button: QAction
    view_processed_button: QAction
    view_final_button: QAction
    view_debug_button: QAction

    def create_toolbar(self) -> None:
        """Create the main window toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.addToolBar(toolbar)
        # toolbar.setMovable(False)

        def toolbar_button_clicked(s: str) -> None:
            print("click", s)

        # open_button_icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        open_button_icon = QIcon("src/preprocessor/icons/fugue16/folder-open-image.png")
        open_button = QAction(open_button_icon, "&Open...", self)
        open_button.setStatusTip("Open an image")
        open_button.triggered.connect(self.on_file_open)
        open_button.setCheckable(False)
        toolbar.addAction(open_button)

        save_button_icon = QIcon("src/preprocessor/icons/fugue16/disk-black.png")
        save_button = QAction(save_button_icon, "&Save...", self)
        save_button.setStatusTip("Save the processed image")
        save_button.triggered.connect(self.on_file_save)
        save_button.setCheckable(False)
        toolbar.addAction(save_button)

        save_all_button_icon = QIcon("src/preprocessor/icons/fugue16/disks-black.png")
        save_all_button = QAction(save_all_button_icon, "Save &All...", self)
        save_all_button.setStatusTip("Save all processed images")
        save_all_button.triggered.connect(self.on_file_save_all)
        save_all_button.setCheckable(False)
        toolbar.addAction(save_all_button)

        toolbar.addSeparator()

        view_group = QtGui.QActionGroup(self)

        view_original_button_icon = QIcon("src/preprocessor/icons/fugue16/image-medium.png")
        self.view_original_button = QAction(view_original_button_icon, "&View Original", view_group)
        self.view_original_button.setStatusTip("View the original image")
        self.view_original_button.triggered.connect(self._on_parameter_change)
        self.view_original_button.setCheckable(True)
        toolbar.addAction(self.view_original_button)

        view_processed_button_icon = QIcon("src/preprocessor/icons/fugue16/image-saturation.png")
        self.view_processed_button = QAction(view_processed_button_icon, "&View Processed", view_group)
        self.view_processed_button.setStatusTip("View the processed image")
        self.view_processed_button.triggered.connect(self._on_parameter_change)
        self.view_processed_button.setCheckable(True)
        # self.view_processed_button.setChecked(True)
        toolbar.addAction(self.view_processed_button)

        view_debug_button_icon = QIcon("src/preprocessor/icons/fugue16/images-flickr.png")
        self.view_debug_button = QAction(view_debug_button_icon, "&View Debug", view_group)
        self.view_debug_button.setStatusTip("View the debug image")
        self.view_debug_button.triggered.connect(self._on_parameter_change)
        self.view_debug_button.setCheckable(True)
        self.view_debug_button.setChecked(True)
        toolbar.addAction(self.view_debug_button)

        view_final_button_icon = QIcon("src/preprocessor/icons/fugue16/image-saturation.png")
        self.view_final_button = QAction(view_final_button_icon, "&View final", view_group)
        self.view_final_button.setStatusTip("View the final image")
        self.view_final_button.triggered.connect(self._on_parameter_change)
        self.view_final_button.setCheckable(True)
        toolbar.addAction(self.view_final_button)

    def create_statusbar(self) -> None:
        """Create the main window status bar."""
        self.statusBar().showMessage(f"Preprocessor {QtGui.QGuiApplication.applicationVersion()} ready")

    def create_central_widget(self) -> None:
        """Create the central widget."""
        self.central_widget = QImageEditor()
        # self.central_widget.setScaledContents(True)
        self.central_widget.setStyleSheet("background-color: purple;")
        self.setCentralWidget(self.central_widget)

    def create_properties_dock(self) -> None:
        """Create a dock widget."""
        # self.properties_dock = cast(QDockWidget, UILoader.load("properties_dock"))
        self.properties_dock = PropertiesDockWidget()
        self.properties_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.properties_dock)

        self.properties_dock.model.on_changed.connect(self._on_parameter_change)

        self.hsv_threshold_widget = HSVThresholdWidget(self.properties_dock.ui.scrollAreaWidgetContents)
        self.properties_dock.ui.layoutScrollAreaPropertiesDock.addWidget(self.hsv_threshold_widget, 7, 0, 1, 1)

    def create_thumbnail_list(self) -> None:
        """Create the thumbnail list dock widget."""
        self.thumbnail_dock = ThumbnailListWidget()
        self.thumbnail_dock.setAllowedAreas(
            Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea
        )
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.thumbnail_dock)
        # When a thumbnail is selected, either show stored result or schedule processing
        self.thumbnail_dock.on_thumbnail_selected.connect(self._display_image)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.write_settings()
        super().closeEvent(event)
        event.accept()

    def write_settings(self) -> None:
        """Write window settings to persistent storage."""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

    def read_settings(self) -> None:
        """Read window settings from persistent storage."""
        self.restoreGeometry(cast(QByteArray, self.settings.value("geometry", QByteArray())))
        self.restoreState(cast(QByteArray, self.settings.value("windowState", QByteArray())))

    def on_file_open(self) -> None:
        # Support opening multiple files
        paths, _ = QFileDialog.getOpenFileNames(self, "Open Images")
        if not paths:
            return
        # Append
        self.thumbnail_dock.model.image_paths = self.thumbnail_dock.model.image_paths + paths

    def on_file_save(self) -> None:
        current_image_path = self._current_image_path
        if not current_image_path:
            return
        # New image path has the `-processed` suffix
        new_image_path_parts = current_image_path.rsplit(".", 1)
        new_image_path: str
        if len(new_image_path_parts) == 2:
            new_image_path = f"{new_image_path_parts[0]}-processed.{new_image_path_parts[1]}"
        else:
            new_image_path = f"{current_image_path}-processed"

        # If no result is available, compute it first (synchronously)
        current_result = self._current_image_result
        if current_result is None:
            try:
                # Synchronously process image using current parameters.
                params = self.properties_dock.model.params
                result = self._process_image(current_image_path, params, None)
                # If processing produced no usable processed image, abort save.
                if result is None or getattr(result, "processed", None) is None:
                    logger.debug(f"No processed result for {current_image_path}; aborting save.")
                    return
                # Store result for future clicks/saves
                try:
                    self.thumbnail_dock.model.set_result_for_path(current_image_path, result)
                except Exception:
                    logger.exception("Failed to store result in thumbnail model after synchronous processing")
                # Update current pointers so UI reflects the new result
                self._current_image_result = result
                current_result = result
            except Exception:
                logger.exception("Synchronous processing for save failed")
                return

        if current_result is None:
            return
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Processed Image", new_image_path)
        if not save_path:
            return
        save_image(save_path, current_result)

    def on_file_save_all(self) -> None:
        save_path = QFileDialog.getExistingDirectory(self, "Select Directory to Save All Processed Images")
        if not save_path:
            return
        image_paths = self.thumbnail_dock.model.image_paths
        if not image_paths:
            return

        params = self.properties_dock.model.params
        import os

        total = len(image_paths)
        progress = QProgressDialog("Processing and saving images...", "Cancel", 0, total, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)

        try:
            for idx, image_path in enumerate(image_paths):
                # handle cancellation
                if progress.wasCanceled():
                    logger.debug("Save-all cancelled by user")
                    break

                filename = os.path.basename(image_path)
                progress.setLabelText(f"Processing {filename} ({idx + 1}/{total})")
                # Keep UI responsive
                QApplication.processEvents()

                # Ensure we have a processed result; compute synchronously if missing
                result = self.thumbnail_dock.model.get_result_for_path(image_path)
                if result is None or getattr(result, "processed", None) is None:
                    try:
                        result = self._process_image(image_path, params, None)
                        if result is None or getattr(result, "processed", None) is None:
                            logger.debug(f"Skipping save for {image_path}: processing failed or produced no processed image")
                            progress.setValue(idx + 1)
                            continue
                        try:
                            self.thumbnail_dock.model.set_result_for_path(image_path, result)
                        except Exception:
                            logger.exception("Failed to store result in thumbnail model after synchronous processing")
                    except Exception:
                        logger.exception(f"Synchronous processing for {image_path} failed")
                        progress.setValue(idx + 1)
                        continue

                # New image path has the `-processed` suffix
                image_path_parts = image_path.rsplit(".", 1)
                if len(image_path_parts) == 2:
                    new_image_path = f"{image_path_parts[0]}-processed.{image_path_parts[1]}"
                else:
                    new_image_path = f"{image_path}-processed"

                # Construct full save path and save
                filename_out = os.path.basename(new_image_path)
                full_save_path = os.path.join(save_path, filename_out)
                try:
                    save_image(full_save_path, result)
                    logger.debug(f"Saved processed image to {full_save_path}")
                except Exception as e:
                    logger.error(f"Failed to save processed image to {full_save_path}", exc_info=e)

                # advance progress and keep UI responsive
                progress.setValue(idx + 1)
                QApplication.processEvents()

        finally:
            progress.close()
            try:
                # Clear any transient message
                self.central_widget.message = ""
            except Exception:
                pass

    def on_help_about(self) -> None:
        show_about_dialog(self)

    _current_image_path: str | None = None
    """Path to the currently displayed image, or None."""
    _current_image_result: QuadratDetectionResult | None = None
    """The result of processing the current image, or None."""
    _latest_token: int = 0
    """Token to identify the latest processing request."""
    _worker_manager: WorkerManager = WorkerManager()

    def _display_image(self, image_path: str) -> None:
        """Display the image: show stored result if available, otherwise schedule processing."""
        self._current_image_path = str(image_path)
        # Check model for existing result
        stored = self.thumbnail_dock.model.get_result_for_path(self._current_image_path)
        if stored is not None and getattr(stored, "processed", None) is not None:
            # Use stored result directly
            self._current_image_result = stored
            self._display_result(stored)
            return
        # schedule background processing
        self._schedule_processing(self._current_image_path)

    def _schedule_processing(self, image_path: str | None) -> None:
        """Schedule a worker to process the image."""
        # Increment token to mark a new request
        self._latest_token += 1
        token = self._latest_token

        # Obtain current parameters
        params = self.properties_dock.model.params

        @Slot(object)
        def on_result(result: QuadratDetectionResult) -> None:
            # pass image_path along so we can store result for the right path
            self._on_process_image_finished(result, token, image_path)

        @Slot(float)
        def on_progress(p: float) -> None:
            self.central_widget.message = f"Processing... {int(p * 100)}%"

        @Slot()
        def act(progress_callback: Signal) -> QuadratDetectionResult:
            # Do not set UI state here (worker thread). Return the result to main thread.
            result = self._process_image(image_path, params, progress_callback)
            return result

        worker = Worker(act)
        worker.signals.result.connect(on_result)
        worker.signals.progress.connect(on_progress)

        try:
            # Clear pixmap and show small text so users know processing is happening
            self.central_widget.pixmap = None
            self.central_widget.message = "Processing..."
        except Exception:
            pass
        self._worker_manager.start(worker)

    def _process_image(
        self, image_path: str | None, params: QuadratDetectionParams, _progress_callback: Signal | None
    ) -> QuadratDetectionResult:
        """Process the image and return it."""
        if not image_path:
            return QuadratDetectionResult(None, None, None, None)

        img = load_image(image_path)
        if img is None:
            return QuadratDetectionResult(None, None, None, None)

        result = detect_quadrat(img, params)
        if params.fix_perspective.enabled and result.corners is not None and len(result.corners) == 4:
            final_img = fix_perspective(
                img,
                result.corners,
                params.fix_perspective.target_width,
                params.fix_perspective.target_height,
            )
            return QuadratDetectionResult(
                original=result.original,
                processed=result.processed,
                final=final_img,
                debug=result.debug,
                corners=result.corners,
            )
        return result

    def _overlay_image(self, base: MatLike, overlay: MatLike) -> MatLike:
        """Overlay one image on top of another with transparency.

        Args:
            base: The base image (H x W x 3).
            overlay: The overlay image with alpha channel (H x W x 4).
        """
        # Extract RGB channels and alpha channel from overlay image
        overlay_rgb = overlay[:, :, :3]
        overlay_alpha = overlay[:, :, 3]
        # Create mask by thresholding alpha channel
        _, base_mask = cv2.threshold(overlay_alpha, 0, 255, cv2.THRESH_BINARY_INV)
        # # Invert mask to create background mask
        # base_mask = cv2.bitwise_not(mask)
        # Apply background mask to background image
        base_masked = cv2.bitwise_and(base, base, mask=base_mask)
        # Combine masked background image and overlay image
        return cv2.bitwise_or(base_masked, overlay_rgb)

    def _display_result(self, result: QuadratDetectionResult) -> None:
        """Display a given processing result in the central widget (main thread)."""
        if result is None or result.processed is None:
            logger.debug("Display skipped: no result")
            return

        try:
            display_img: MatLike | None
            if self.view_original_button.isChecked():
                display_img = result.original
            elif self.view_processed_button.isChecked():
                display_img = result.processed
            elif self.view_debug_button.isChecked():
                display_img = result.debug
            elif self.view_final_button.isChecked():
                display_img = result.final
            else:
                display_img = None  # will be handled below

            qimg = array2qimage(display_img)
            qpixmap = QtGui.QPixmap.fromImage(qimg)
            self.central_widget.pixmap = qpixmap
            self.central_widget.message = ""
        except Exception as e:
            logger.error("Error displaying image", exc_info=e)
            self.central_widget.message = f"Error: {e}"

    def _on_process_image_finished(self, result: QuadratDetectionResult, token: int, image_path: str | None) -> None:
        """Handle worker finished processing the image."""
        # Only update the display if this is the latest request
        if token != self._latest_token:
            logger.debug("Finishing processing, skipped: not latest")
            return
        # Only update the display if there is a result
        if result is None or result.processed is None:
            logger.debug("Finishing processing, skipped: no result")
            return

        # Store result in the thumbnail model for this path (so subsequent clicks reuse it)
        if image_path:
            try:
                self.thumbnail_dock.model.set_result_for_path(image_path, result)
            except Exception:
                logger.exception("Failed to store result in thumbnail model")

        # Update current pointers
        self._current_image_result = result

        # Display result (we are already on main thread because signal handlers run on main)
        try:
            self._display_result(result)
        except Exception as e:
            logger.error("Error scheduling display", exc_info=e)
            self.central_widget.message = f"Error: {e}"




